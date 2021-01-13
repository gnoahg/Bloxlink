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
	"BANNED": "<:ban:476838302092230672>"
}

RETHINKDB_HOST = "rethinkdb"
RETHINKDB_PASSWORD = None
RETHINKDB_PORT = 28015
RETHINKDB_DB = "bloxlink"

REDIS_HOST = "redis"
REDIS_PORT = 6379
REDIS_PASSWORD = None

TOKEN = "Nzk4NTY0NTAwNTUwNTgyMzEy.X_23JQ.6dDo8H6UTKxc3QuvveYQfNaEFh0"

BLOXLINK_GUILD = 782417658615824385 # your guild ID, used to load nitro boosters and other data
	