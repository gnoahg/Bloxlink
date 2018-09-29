from discord.errors import Forbidden

from resources.module import get_module
parse_message = get_module("commands", attrs=["parse_message"])
post_event = get_module("utils", attrs=["post_event"])
verify_member, give_roblox_stuff, get_user = get_module("roblox", attrs=[
	"verify_member",
	"give_roblox_stuff",
	"get_user"
	]
)


async def setup(**kwargs):
	command = kwargs.get("command")

	@command(name="switchuser", category="Account", aliases=["switchaccount"])
	async def switchuser(message, response, args, prefix):
		"""change your account for the server"""

		author = message.author
		guild = message.guild
		roblox_user, accounts = await get_user(author=author)

		if roblox_user or accounts:
			if accounts:
				parsed_args, is_cancelled = await args.call_prompt([
					{
						"prompt": "Which account would you like to verify as _for this server_?\n" \
							"**Account IDs:** " + ", ".join(accounts),
						"type": "choice",
						"choices": accounts,
						"name": "acc"
					},
					{
						"prompt": "Would you like to set this account as your **primary** account?",
						"type": "choice",
						"choices": ["yes", "no"],
						"name": "primary"
					},
					{
						"prompt": "Please note: this will remove all your roles and give you roles " \
							"depending on the server configuration. Continue?",
						"type": "choice",
						"choices": ["yes", "no"],
						"name": "continue"
					}
				])

				if not is_cancelled:
					if parsed_args["continue"] == "yes":
						await verify_member(author, parsed_args["acc"], primary_account=parsed_args["primary"] == "yes")

						if parsed_args["primary"] == "yes":
							await response.success("**Saved** your new primary account!")

						roles = list(author.roles)
						roles.remove(guild.default_role)

						try:
							await author.remove_roles(*roles, reason="Switched User— cleaning their roles")
						except Forbidden:
							await post_event(
								"error",
								f"Failed to delete roles from {author.mention}. Please ensure I have " \
									"the ``Manage Roles`` permission, and drag my role above the other roles.",
								guild=guild,
								color=0xE74C3C
							)

						new_user, _ = await get_user(id=parsed_args["acc"])
						await new_user.fill_missing_details()

						await give_roblox_stuff(author, complete=True)

						await post_event("verify", f"{author.mention} is now verified as **{new_user.username}.**", guild=guild, color=0x2ECC71)

						await response.success("You're now verified as **"+new_user.username+"!**")
			else:
				await response.error(f"You only have **one account** linked! Run ``{prefix}verify -add`` to link another.")
		else:
			message.content = f"{prefix}verify"
			return await parse_message(message)