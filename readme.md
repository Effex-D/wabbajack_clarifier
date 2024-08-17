### Getting Started

#### Install Python3 and the Requests Library

Google how to do this if you're not sure. The internet has better explanations than I.

#### Get a Nexus Mods API key

1) Get a NexusMods API key from (here)[https://www.nexusmods.com/users/myaccount?tab=api%20access]
2) Set the API key as an evironmental variable
```
export NEXUS_API_KEY=YourAPIKey
```

#### Identify your game

Find out the name of your game. It's usually fairly obvious from the main Nexusmods URL. Example:

https://www.nexusmods.com/skyrimspecialedition

#### Get the Wabbajack File

The next thing you need to do is get the Wabbajack file, which will typically be some sort of archive like .7z or .rar. 

Extract the file using whatever software on whatever operating system you have. 7z tends to work nicely for Windows.

When you extract the file, you'll have a file with a .wabbajack extension. This is actually also just an archive, meaning you can open it up with 7zip to grab what's inside.

You need a file called modlist, without a file extension. Don't let it lie to you. This file is actually just a JSON file containing information about all the mods. If you're comfortable using JSON you can just look through this file. However, the python scripts here are designed to format the useful information to CSV which can be imported into Google Docs.

### Runtime

#### Phase 1

Phase 1 is easy. Run the file "create_csv_from_modlist.py" like so:

```
python3 create_csv_from_modlist.py
```

This will output a file which contains the mod name and the short summary from the modlist.

#### Expanding with Categories

If you want more information, run the file "create_csv_with_categories.py" like so:

```
python3 create_csv_with_categories.py <gamename>
```

This should output the final CSV file, but it is contingent on Phase1 being run first. This is probably not ideal, but as this was hacked together in 12 minutes, I'm perfecty okay with it. If you want to improve it, go ahead.

