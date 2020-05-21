from resources.structures.Bloxlink import Bloxlink # pylint: disable=import-error
from discord.errors import Forbidden, NotFound
from discord import Embed
from os import environ as env
from resources.exceptions import Message, UserNotVerified, Error, RobloxNotFound, BloxlinkBypass # pylint: disable=import-error
from resources.constants import DEFAULTS, NICKNAME_TEMPLATES # pylint: disable=import-error
from aiotrello.exceptions import TrelloNotFound, TrelloUnauthorized, TrelloBadRequest

verify_as, update_member, get_user, get_nickname, get_roblox_id = Bloxlink.get_module("roblox", attrs=["verify_as", "update_member", "get_user", "get_nickname", "get_roblox_id"])
get_options = Bloxlink.get_module("trello", attrs="get_options")

try:
    from config import TRELLO
except ImportError:
    TRELLO = {
        "KEY": env.get("TRELLO_KEY"),
        "TOKEN": env.get("TRELLO_TOKEN"),
	    "TRELLO_BOARD_CACHE_EXPIRATION": 5 * 60,
	    "GLOBAL_CARD_LIMIT": 100
    }

@Bloxlink.command
class VerifyCommand(Bloxlink.Module):
    """link your Roblox accont to your Discord account"""

    def __init__(self):
        self.examples = ["add", "unlink"]


    @staticmethod
    async def validate_username(message, content):
        try:
            roblox_id, username = await get_roblox_id(content)
        except RobloxNotFound:
            return None, "There was no Roblox account found with that username. Please try again."

        return username

    @Bloxlink.flags
    async def __main__(self, CommandArgs):
        trello_board = CommandArgs.trello_board
        guild_data = CommandArgs.guild_data
        guild = CommandArgs.message.guild
        author = CommandArgs.message.author

        if CommandArgs.flags.get("add") or CommandArgs.flags.get("verify") or CommandArgs.flags.get("force"):
            await CommandArgs.response.error(f"``{CommandArgs.prefix}verify --force`` is deprecated and will be removed in a future version of Bloxlink. "
                                             f"Please use ``{CommandArgs.prefix}verify add`` instead.")

        username = len(CommandArgs.string_args) >= 1 and CommandArgs.string_args[0]
        if username:
            return await self.add(CommandArgs)

        trello_options = {}

        if trello_board:
            trello_options, _ = await get_options(trello_board)
            guild_data.update(trello_options)

        try:
            _, _, _, _, roblox_user = await update_member(
                    CommandArgs.message.author,
                    guild                = guild,
                    guild_data           = guild_data,
                    roles                = True,
                    nickname             = True,
                    trello_board         = CommandArgs.trello_board,
                    author_data          = await self.r.table("users").get(str(author.id)).run(),
                    given_trello_options = True)

        except BloxlinkBypass:
            raise Message("Since you have the ``Bloxlink Bypass`` role, I was unable to update your roles/nickname.", type="info")

        except UserNotVerified:
            await self.add(CommandArgs)
        else:

            welcome_message = guild_data.get("welcomeMessage", DEFAULTS.get("welcomeMessage"))
            welcome_message = await get_nickname(author, welcome_message, guild_data=guild_data, roblox_user=roblox_user, is_nickname=False)

            raise Message(welcome_message)


    @Bloxlink.subcommand()
    async def add(self, CommandArgs):
        """link a new account to Bloxlink"""

        author = CommandArgs.message.author
        guild = CommandArgs.message.guild

        guild_data = CommandArgs.guild_data
        trello_board = CommandArgs.trello_board

        response = CommandArgs.response

        username = len(CommandArgs.string_args) >= 1 and CommandArgs.string_args[0]

        args = []

        if not username:
            args.append({
                "prompt": "What's the username of your Roblox account?",
                "type": "string",
                "name": "username",
                "validation": self.validate_username
            })

        args.append({
            "prompt": "Would you like to set this as your default Roblox account for new servers? ``yes/no``",
            "name": "default",
            "type": "choice",
            "choices": ["yes", "no"]
        })

        args = await CommandArgs.prompt(args, dm=True)
        username = username or args["username"]

        # TODO: if groupVerify is enabled, they must join the roblox group(s) to be able to verify. bypasses the cache.
        # groupVerify = [group_ids...]

        trello_options = {}

        if trello_board:
            trello_options, _ = await get_options(trello_board)
            guild_data.update(trello_options)

        try:
            username = await verify_as(
                author,
                guild,
                response = CommandArgs.response,
                primary  = args["default"] == "yes",
                username = username,
                trello_options = trello_options,
                update_user = False)

        except Message as e:
            if e.type == "error":
                await response.error(e)
            else:
                await response.send(e)
        except Error as e:
            await CommandArgs.response.error(e, dm=True, no_dm_post=True)
        else:
            try:
                added, removed, nickname, errors, roblox_user = await update_member(
                    author,
                    guild                = guild,
                    guild_data           = CommandArgs.guild_data,
                    roles                = True,
                    nickname             = True,
                    author_data          = await self.r.table("users").get(str(author.id)).run(),
                    given_trello_options = True)

            except BloxlinkBypass:
                await response.info("Since you have the ``Bloxlink Bypass`` role, I was unable to update your roles/nickname; however, you were still linked to Bloxlink.", dm=True, no_dm_post=True)

                return

            welcome_message = (trello_options.get("welcomeMessage", "")) or guild_data.get("welcomeMessage", DEFAULTS.get("welcomeMessage"))

            welcome_message = await get_nickname(author, welcome_message, guild_data=guild_data, roblox_user=roblox_user, is_nickname=False)

            await response.send(welcome_message, dm=True, no_dm_post=True)


    @Bloxlink.subcommand(permissions=Bloxlink.Permissions().build("BLOXLINK_MANAGER"))
    async def customize(self, CommandArgs):
        """customize the behavior of !verify"""

        # TODO: able to set: "forced groups", allowReVerify

        prefix = CommandArgs.prefix
        guild = CommandArgs.message.guild
        response = CommandArgs.response


        choice = (await CommandArgs.prompt([{
            "prompt": "Which option would you like to change?\nOptions: ``(welcomeMessage)``",
            "name": "choice",
            "type": "choice",
            "choices": ("welcomeMessage",)
        }]))["choice"]


        trello_board = CommandArgs.trello_board
        card = None

        if trello_board:
            options_trello_data, trello_binds_list = await get_options(trello_board, return_cards=True)
            options_trello_find = options_trello_data.get(choice)

            if options_trello_find:
                card = options_trello_find[1]

        if choice == "welcomeMessage":
            welcome_message = (await CommandArgs.prompt([{
                "prompt": f"What would you like your welcome message to be? This will be shown in ``{prefix}verify`` messages.\nYou may "
                           f"use these templates: ```{NICKNAME_TEMPLATES}```",
                "name": "welcome_message",
                "formatting": False,
                "max": 1500
            }]))["welcome_message"]

            if trello_board:
                try:
                    if card:
                        if card.name == choice:
                            await card.edit(name="welcomeMessage", desc=welcome_message)
                    else:
                        trello_settings_list = await trello_board.get_list(lambda L: L.name == "Bloxlink Settings") \
                                            or await trello_board.create_list(name="Bloxlink Settings")

                        await trello_settings_list.create_card(name="welcomeMessage", desc=welcome_message)

                    await trello_binds_list.sync(card_limit=TRELLO["GLOBAL_CARD_LIMIT"])

                except TrelloUnauthorized:
                    await response.error("In order for me to edit your Trello settings, please add ``@bloxlink`` to your "
                                         "Trello board.")

                except (TrelloNotFound, TrelloBadRequest):
                    pass

            await self.r.db("canary").table("guilds").insert({
                "id": str(guild.id),
                "welcomeMessage": welcome_message
            }, conflict="update").run()

        raise Message(f"Successfully saved your new ``{choice}``!", type="success")


    @staticmethod
    @Bloxlink.subcommand()
    async def view(CommandArgs):
        """view your linked account(s)"""

        raise NotImplementedError

    @staticmethod
    @Bloxlink.subcommand()
    async def unlink(CommandArgs):
        """unlink an account from Bloxlink"""

        raise NotImplementedError
