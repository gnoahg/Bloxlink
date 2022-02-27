from resources.constants import RELEASE, IS_DOCKER # pylint: disable=import-error

# More optional settings can be set, such as a Trello key/token. Look at the docker-compose.yml for additional values.

PREFIX = "!"

WEBHOOKS = { # discord webhook links
	"LOGS":  "https://discord.com/api/webhooks/798940930275016795/jsgzRsHAKIqyZA1QHL9k-o2XVyVLlFPJXMaWSzcASQGe4fZq3EmgJQZHieer-u3-YIYL",
	"ERRORS": "https://discord.com/api/webhooks/798940712287862844/vpfHdizTPg8JD71T1411RGiljZ2WkoD-WAcRocOr8-wVipySIbS4x0Dsbgm-VhXZ_3Df"
}

REACTIONS = { # discord emote mention strings
	"LOADING": "<a:BloxlinkLoading:530113171734921227>",
	"DONE": "<:BloxlinkSuccess:506622931791773696>",
	"DONE_ANIMATED": "<a:BloxlinkDone:528252043211571210>",
	"ERROR": "<:BloxlinkError:506622933226225676>",
	"VERIFIED": "<a:Verified:734628839581417472>",
	"BANNED": "<:ban:476838302092230672>",
	"RED": "<:red:881780174151110656>",
	"REPLY": "<:Reply:872019019677450240>",
	"REPLY_END": ":ReplyCont:872018974831968259>",
	"GREEN": "<:green:881783400632037426>",
	"BLANK": "<:blank:881783214014885908>"
}

RETHINKDB_HOST = "rethinkdb"
RETHINKDB_PASSWORD = None
RETHINKDB_PORT = 28015
RETHINKDB_DB = "bloxlink"

REDIS_HOST = "redis"
REDIS_PORT = 6379
REDIS_PASSWORD = None

TOKEN = "Nzk4NTY0NTAwNTUwNTgyMzEy.X_23JQ.6dDo8H6UTKxc3QuvveYQfNaEFh0"

<<<<<<< HEAD
BLOXLINK_GUILD = None # your guild ID, used to load nitro boosters and other data

BOTS = {
	"PRO": 469652514501951518,
	"MAIN": 426537812993638400,
	"CANARY": 442912486702710784,
	"LOCAL": 454053406471094282
}

RESTRICTIONS_TRELLO = "" # Your Trello board link to load restrictions.
						 # Board must have 3 lists: "Roblox IDs", "Discord IDs", and "Servers"
						 # Card format:
						 	# card name: label:id
							# card desc: restriction text
							# The label has no effect on restrictions. It's for visual purposes only.
=======
BLOXLINK_GUILD = 782417658615824385 # your guild ID, used to load nitro boosters and other data
	
>>>>>>> 6d160ab00a17079a61d360cd861d7bd3b15992af
