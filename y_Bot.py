#! /usr/bin/python3
import discord
from fractions import Fraction

class Y_Bot_Exception(Exception):
    pass

def parse_command(command, the_list_of_commands, allow_abbreviations=True):
    the_list_that_we_pair_down = the_list_of_commands[:]
    if allow_abbreviations:
        i = 0
        while i < len(command):
            j = 0
            while j < len(the_list_that_we_pair_down):
                if the_list_that_we_pair_down[j][i] != command[i]:
                    del the_list_that_we_pair_down[j]
                    j -= 1
                j += 1
            i += 1
            
        if len(the_list_that_we_pair_down) == 1:
            return the_list_that_we_pair_down[0]
        elif len(the_list_that_we_pair_down) == 0:
            raise Y_Bot_Exception(f"Command not found: {command}")
        else:
            raise Y_Bot_Exception(f"Ambigous command \"{command}\"", f"possibilites are: {', '.join(the_list_that_we_pair_down)}")

async def do_command(command, message, the_rest_of_the_command):
    if command == "ping":
        await message.channel.send("pong")
    elif command == "pong":
        await message.channel.send("ping")
    elif command == "conv":
        the_rest_of_the_command = the_rest_of_the_command.split()
        the_strings_in_the_rest_of_the_command_that_actually_matter = the_rest_of_the_command[:min(len(the_rest_of_the_command), 3)]
        the_three_ratios = [Fraction(x) for x in the_strings_in_the_rest_of_the_command_that_actually_matter]
        if len(the_rest_of_the_command) == 2:
            the_three_ratios.append(Fraction())
        if len(the_rest_of_the_command) == 4:
            should_it_be_a_float = True
        else:
            should_it_be_a_float = False;
        the_linear_equation = the_three_ratios[0] * the_three_ratios[1] + the_three_ratios[2]
        await message.channel.send(str(the_linear_equation) if not should_it_be_a_float else str(float(the_linear_equation)))

class Y_Bot(discord.Client):
    async def on_ready(self):
        print(f"Logged in as {self.user}")
    async def on_message(self, message):
        the_list_of_commands = ["ping", "pong", "conv"]
        if message.content[0:5] == "ybot;":
            the_command_without_start = message.content[5:].split()[0] if len(message.content[5:]) != 0 else ""
            the_rest_of_the_command = ' '.join(message.content[5:].split()[1:]) if len(message.content[5:].split()) > 1 else None
            print(the_command_without_start)
            try:
                await do_command(parse_command(the_command_without_start, the_list_of_commands), message, the_rest_of_the_command)
            except Y_Bot_Exception as y:
                embed = discord.Embed(title=y.args[0], description="You made an error" if len(y.args) == 1 else y.args[1], color=0xff0000)
                await message.channel.send(embed=embed)

y_Bot = Y_Bot()
with open("auth") as auth:
    token = auth.read()[:-1]
    y_Bot.run(token)
