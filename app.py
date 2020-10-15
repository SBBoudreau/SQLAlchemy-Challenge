from flask import Flask, jsonify

justice_league_members = [
    {"superhero": "Aquaman", "real_name": "Arthur Curry"},
    {"superhero": "Batman", "real_name": "Bruce Wayne"},
    {"superhero": "Cyborg", "real_name": "Victor Stone"},
    {"superhero": "Flash", "real_name": "Barry Allen"},
    {"superhero": "Green Lantern", "real_name": "Hal Jordan"},
    {"superhero": "Superman", "real_name": "Clark Kent/Kal-El"},
    {"superhero": "Wonder Woman", "real_name": "Princess Diana"}
]

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/api/v1.0/justice-league")
def justice_league():
    """Return the justice league data as json"""

    return jsonify(justice_league_members)


@app.route("/")
def welcome():
    return (
        f"Welcome to the Justice League API!<br/><br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/justice-league<br/>"
        f"/api/v1.0/justice-league/real-name/SUPERHERO_REAL_NAME"
    )

## Until this point, we've been executing functions without any arguments
# and with static endpoint routes.
# Here we can decide how the route's function should run, based on
# the value used in the URL.

@app.route("/api/v1.0/justice-league/real-name/<real_name>")
def justice_league_character(real_name):
    """Fetch the Justice League character whose real_name matches
       the path variable supplied by the user, or a 404 if not."""

    # replace the space and lowercase the value so "Bruce Wayne" becomes "brucewayne"
    # which will make the dictionary comparison simpler.
    search_term = real_name.replace(" ", "").lower()

    # loop over the justice league list of dictionaries and 
    # if a match is found, jsonify the character's dictionary and return it
    # if not, then return an error
    for character in justice_league_members:
        real_name_lowered = character["real_name"].replace(" ", "").lower()

        if real_name_lowered == search_term:
            return jsonify(character)

    return jsonify({"error": f"Character with real_name {real_name} not found."}), 404


# run in development mode
if __name__ == "__main__":
    app.run(debug=True)
