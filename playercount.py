#!/usr/bin/python3
import valve.source.a2s as a2
s=a2.ServerQuerier("atlantishq.de",27015)
print(s.players()["player_count"])
s.close()
