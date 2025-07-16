import discord

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

    if user_id not in todo_lists:
        todo_lists[user_id] = []

    if command.lower() == "!add":
        task = " ".join(args)
        todo_lists[user_id].append(task)
        await message.channel.send(f"Task '{task}' added to your to-do list.")

    elif command.lower() == "!list":
        tasks = todo_lists.get(user_id, [])
        if not tasks:
            await message.channel.send("Your to-do list is empty!")
        else:
            task_list = "\n## ".join(f"{idx+1}. {task}" for idx, task in enumerate(tasks))
            await message.channel.send(f"# Your to-do list: \n## {task_list}")

    elif command.lower() == "!remove":
        try:
            task_number = int(args[0]) - 1
            removed_task = todo_lists[user_id].pop(task_number)
            await message.channel.send(f"Removed task '{removed_task}' from your to-do list.")
        except (IndexError, ValueError):
            await message.channel.send("Invalid task number! Use !list to check task numbers.")

    elif command.lower() == "!finished":
        try:
            task_number = int(args[0]) - 1
            print(todo_lists[user_id][task_number])
            todo_lists[user_id][task_number] = "~~" + todo_lists[user_id][task_number] + "~~"
        except (IndexError, ValueError):
            await message.channel.send("Invalid task number! Use !list to check task numbers.")

client.run(TOKEN)