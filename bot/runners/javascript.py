import re
import json
import aiohttp
import nextcord


class JavascriptInterpreter:
    async def exec(self, message: nextcord.Message, content: str):
        title = "✅ Exec Javascript - Success"
        color = 0x00FF00

        code, user_input = re.match(
            r"^.*?```(?:js|javascript)?\s*(.+?)\s*```\s*(.+)?$", content, re.DOTALL
        ).groups()

        async with aiohttp.ClientSession() as session:
            data = {'run': code}
            async with session.post('http://92.222.231.56:27030/run', data=data) as response:
                if response.status != 200:
                    return

                config = {
                    "fatal": {
                        "text": "Fatal Error",
                        "icon": "❌",
                        "color": 0xFF0000
                    },
                    "error": {
                        "text": "Error",
                        "icon": "❌",
                        "color": 0xFF0000
                    },
                    "warn": {
                        "text": "Warning",
                        "icon": ":warning:",
                        "color": 0xFFCC4D
                    },
                    "info": {
                        "text": "Info",
                        "icon": ":information_source:",
                        "color": 0x2D51AD
                    },
                    "default": {
                        "text": "Successful",
                        "icon": "✅",
                        "color": 0x00FF00
                    },
                }

                header = " Exec JavaScript - "

                result = await response.json()
                out = ""
                for line in result:
                    args = []
                    try:
                        title = config[line["type"]]["icon"] + header + config[line["type"]]["text"]
                        color = config[line["type"]]["color"]
                    except:
                        title = config["default"]["icon"] + header + config["default"]["text"]
                        color = config["default"]["color"]

                    if line["type"] == "fatal":
                        args = str(line["args"][0]["stack"])
                    else:
                        args = [str(arg) for arg in line["args"]]

                    if type == "timeEnd":
                        args = args[1:]

                    for i in range(0, len(args)):
                        if args[i] is None or args[i] == "null" or args[i] == "None":
                            args[i] = "undefined"

                    out = out + " ".join(args) + "\n"

                old_out = out
                if out.count("\n") > 30:
                    lines = out.split("\n")
                    out = "\n".join(
                        lines[:15]
                        + [f".\n.\nRemoved {len(lines) - 30} lines\n.\n."]
                        + lines[-17:]
                    )
                if len(out) > 1000:
                    out = (
                            old_out[:497]
                            + f"\n.\n.\nRemoved {len(old_out) - 1000} characters\n.\n.\n"
                            + old_out[-504:]
                    )

                if len(result) == 0:
                    title = ":radio_button: Exec Javascript"
                    color = 0x2d51ad
                    out = "*No output or exceptions*"

                await message.channel.send(
                    embed=nextcord.Embed(
                        title=title, description=f"```\n{out}\n```", color=color
                    ),
                    reference=message,
                    allowed_mentions=nextcord.AllowedMentions(replied_user=True),
                )