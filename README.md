# Session Tracks

Build up your character and try your luck in the battleground arena.

Walkthrough the evergreen forest to the Waystone Inn and help Kote to defeat its property against the forest beasts. All kinds of interesting adventures await you.

# Project structure

The project is made using gRPC to simulate microservices in python. There are 2 microservices.
- `Characters` that holds information about different character type `Human` or `Beasts`
   - The character stats are generate randomly between some predefined ranges
- `Batteground` services will have the logic to decide who will be the winner in an epic battle between two caracters.
  - The battle winner is decide after 20 rounds or after one of the players has less than 0 health
  - A BattleLog will be saved and returned 

An additional container will start a webnode that will be accesible on `localhost:5000`. A small UI will quide you to the battle.

# Start swagger webserver locally

The entire project is dockeriezed and a single docker-compose file should be used

```
> docker-compose -f dockerfiles/docker-compose.yml build
> docker-compose -f dockerfiles/docker-compose.yml up -d webserver
```

# Run tests

All the dependecies of the code are present in a docker image.

```
> docker-compose -f dockerfiles/docker-compose.yml build
> docker-compose -f dockerfiles/docker-compose.yml up tests
```
