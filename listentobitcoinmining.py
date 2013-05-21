################################################################################
# 
# Copyright (c) 2011 fpgaminer@bitcoin-mining.com
#
#
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.
################################################################################
import pyglet
import cgminer_api
import time
import random
import glob
import argparse
from threading import Thread


def _log (data):
	print "[%s]" % time.strftime ('%H:%M:%S'), data


class MinerModel (object):
	def __init__ (self, host, port=4028):
		self.shares_per_second = 0
		self.last_share_count = None
		self.last_update = None
		self.host = host
		self.port = port

		self.work = 0
		self.mining_rate = 0
		self.since_last_sound = 0
	
	def update (self):
		data = cgminer_api.api_request ('summary', self.host, self.port)
		query_time = time.time ()

		try:
			share_count = float (data['SUMMARY'][0]['Difficulty Accepted'])
		except:
			_log ("%s:%d failed to respond to API request." % (self.host, self.port))
			self.shares_per_second = 0
			self.last_share_count = None
			self.last_update = query_time
			return

		share_count = int (share_count)

		if self.last_share_count is not None:
			if share_count < self.last_share_count:
				# Miner must have restarted
				self.last_share_count = 0

			diff = share_count - self.last_share_count
			self.work += diff
			self.shares_per_second = diff / (query_time - self.last_update)

		self.last_share_count = share_count
		self.last_update = query_time

		hashrate = int (self.shares_per_second * 2**32 / 1000000)
		_log ("%s:%d\t%.02f S/s\t%d MH/s" % (self.host, self.port, self.shares_per_second, hashrate))
	
	def mine (self, dt):
		if self.work < minimum_work:
			self.mining_rate = 0.0
			#_log ("Taking a break")
			return

		self.since_last_sound += dt

		# Work at least this hard
		self.mining_rate = max (self.mining_rate, minimum_mining_rate)

		# How fast do we need to work on average, to finish in two minutes
		needed_rate = (self.work / shares_per_sound) / 120.0
		ratio = needed_rate / self.mining_rate

		#_log ("Rate: %f" % self.mining_rate)
		#_log ("Work: %d" % self.work)
		#_log ("Needed: %f, ratio: %f" % (needed_rate, ratio))

		# Adjust our current mining rate
		if ratio > 2.0 or ratio < 0.5:
			difference = needed_rate - self.mining_rate
			self.mining_rate += difference * random.gauss (0.5, 0.2)
			#_log ("Mining rate adjusted: %f" % self.mining_rate)

		# Occasionally adjust rate randomly
		if random.random () < (dt * 0.2):
			self.mining_rate *= random.gauss (2.0, 1.0)

		# Bound
		self.mining_rate = max (self.mining_rate, minimum_mining_rate)

		# Time between sounds
		delta = 1.0 / self.mining_rate

		#_log ("Wavelength: %f, time: %f" % (delta, self.since_last_sound))

		# Now mine!
		if self.since_last_sound < delta:
			return

		self.since_last_sound = 0# - delta
		random.choice (sounds).play ()
		self.work = max (0, self.work - shares_per_sound)


def stats_updater ():
	while True:
		# Query all the miners
		for miner in miners:
			miner.update ()

		# Nap time
		time.sleep (stats_interval)


def audio_updater (dt):
	for miner in miners:
		miner.mine (dt)


# Read command line
parser = argparse.ArgumentParser (description='Bitcoin Mining Audio Landscape')
parser.add_argument ('miners', metavar='CGMINER', nargs='+', help='cgminer IP, e.g. 127.0.0.1:4028')
parser.add_argument ('--shares-per-sound', dest='shares_per_sound', action='store', type=int, default=10, help='Play 1 sound for every X shares')

args = parser.parse_args ()


# Settings
shares_per_sound = args.shares_per_sound   # Play 1 sound for every X shares
minimum_work = 50           # When to take a break from mining
minimum_mining_rate = 0.5   # Minimum number of sounds per second, when not taking a break
audio_interval = 0.1        # How often to call the audio update function
stats_interval = 30         # How often to update miner stats


# Build list of miners
miners = []
for url in args.miners:
	url = url.split (':')

	if len (url) == 1:
		host,port = url[0],4028
	else:
		host,port = url

	miners.append (MinerModel (host=host, port=int(port)))


# Load sounds
sounds = []
for filename in glob.glob ('./audio/*.wav'):
	sounds.append (pyglet.media.load (filename, streaming=False))


# Events
stats_thread = Thread (target=stats_updater)
stats_thread.daemon = True
stats_thread.start ()
pyglet.clock.schedule_interval (audio_updater, audio_interval)


# Run
pyglet.app.run ()
stats_timer.cancel ()
