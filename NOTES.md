
# Requirements

- Configuration files (TOML)
    - ability to reload and apply modified config?
- Multiple Networks
- Per channel encoding? Or only per Network (Connection).
- Commands
- Timed commands (rss reader)
- Some form of storage
- Addons
    - start processes
    - read data from sockets
    - limit addon to conditions (network/channel/user/message-type)
    - access storage


# IRC Bot structure

- asyncio, py3.5 with async/await
- typing module
- parsing core
    - a raw line to a Message
    - a Message to a raw line
- state core
    - Networks
        - server list
        - channel list
        - user list
    - addons
