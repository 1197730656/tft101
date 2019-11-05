import requests
from datetime import datetime

class RiotAPI(object):
	def __init__(self, api_key, region, tftregion):
		self.api_key = api_key
		self.region = region
		self.tftregion = tftregion
		self.headers = {"X-Riot-Token": api_key}

	def get_summoner(self, name):
		url = "https://{}.api.riotgames.com/tft/summoner/v1/summoners/by-name/{}".format( self.region, name)
		res = requests.get(url=url, headers=self.headers)
		return Summoner(res.json())

	def get_matches(self, summoner, begin_index=-1, end_index=-1):
		url = "https://{}.api.riotgames.com/lol/match/v4/matchlists/by-account/{}".format(self.region, summoner.accountId)
		url += "?"
		if begin_index >= 0:
			url += "beginIndex={}".format(begin_index)
			if end_index >= 0:
				url += "&"
		if end_index >= 0:
			url += "endIndex={}".format(end_index)
		res = requests.get(url=url, headers=self.headers)
		return res.json()

	def get_tft_match_ids(self, summoner):
		url = "https://{}.api.riotgames.com/tft/match/v1/matches/by-puuid/{}/ids".format(self.tftregion, summoner.puuid)
		res = requests.get(url=url, headers=self.headers)
		return res.json()

	def get_tft_match(self, match_id):
		url = "https://{}.api.riotgames.com/tft/match/v1/matches/{}".format(self.tftregion, match_id)
		res = requests.get(url=url, headers=self.headers)
		return res.json()

	def get_tft_matches(self, summoner):
		match_data = []
		for match_id in self.get_tft_match_ids(summoner):
			match_data.append(self.get_tft_match(match_id))
		return match_data


class Summoner(object):
	def __init__(self, data):
		self.id = data['id']
		self.accountId = data['accountId']
		self.puuid = data['puuid']
		self.name = data['name']
		self.profileIconId = data['profileIconId']
		self.revisionDate = datetime.utcfromtimestamp(data['revisionDate'] / 1000)
		self.level = data['summonerLevel']

	