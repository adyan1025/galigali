import discord
import cal

intents = discord.Intents.default()
intents.message_content = True
client = discord.Client(intents=intents)

TOKEN = ""
try:
    with open("api_key.txt", "r") as file:
        TOKEN = file.read()
except FileNotFoundError:
    print("Error: The file 'my_file.txt' was not found.")
except Exception as e:
    print(f"An error occurred: {e}")

todo_lists = {}

@client.event
async def on_ready():
    print(f'{client.user} has connected to Discord!')

@client.event
async def on_message(message):
    if message.author == client.user:
        return
    
    if not message.content.strip():
            return
    
    command, *args = message.content.split()
    user_id = str(message.author.id)

    def create_todo():
        tasks = todo_lists.get(user_id, [])
        if not tasks:
            return "> Your to-do list is empty!"
        else:
            task_list = "\n> ".join(f"{idx+1}. {task}" for idx, task in enumerate(tasks))
            todo = f"**To-Do List:** \n> {task_list}"
            return todo


    if user_id not in todo_lists:
        todo_lists[user_id] = []

    if command.lower() == "!add" or command.lower() == "!a":
        task = " ".join(args)
        todo_lists[user_id].append(task)
        await message.channel.send(f"> Task '{task}' added to your to-do list.\n" + create_todo())

    if command.lower() == "!addmore" or command.lower() == "!am":
        await message.channel.send("```Listening... (type 'stop' to stop)```")
        def check(m):
            return m.author == message.author
        while True:
            try:
                response_message = await client.wait_for('message', check=check)
                task = response_message.content
                if task.startswith('!'):
                    await message.channel.send("> Commands are disabled while adding more tasks. Type 'stop' to finish.")
                    continue
                if task.lower() == "stop":
                    await message.channel.send(create_todo())
                    break
                todo_lists[user_id].append(task)
                await message.channel.send(f"> Task '{task}' added to your to-do list.")
            except Exception as e:
                await message.channel.send("> An error occurred. Please try again.")
                break

    elif command.lower() == "!list" or command.lower() == "!l":
        await message.channel.send(create_todo())

    elif command.lower() == "!remove" or command.lower() == "!r":
        try:
            task_number = int(args[0]) - 1
            removed_task = todo_lists[user_id].pop(task_number)
            await message.channel.send(f"> Removed task '{removed_task}' from your to-do list.\n\n" + create_todo())
        except (IndexError, ValueError):
            await message.channel.send("> Invalid task number! Use !list to check task numbers.")

    elif command.lower() == "!finished" or command.lower() == "!f":
        try:
            task_number = int(args[0]) - 1
            todo_lists[user_id][task_number] = "~~" + todo_lists[user_id][task_number] + "~~"
            await message.channel.send(create_todo())
        except (IndexError, ValueError):
            await message.channel.send("Invalid task number! Use !list to check task numbers.")

    elif command.lower() == "!calendar" or command.lower() == "!c":
        try:
            events = cal.calendar_api()
            await message.channel.send(events)
        except Exception as e:
            await message.channel.send(f"Calendar is unavailable due to an error: {e}")

client.run(TOKEN)