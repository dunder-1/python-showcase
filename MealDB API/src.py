import json, requests
from dataclasses import dataclass

def get_json(url:str, save_in_db=True) -> dict:
    """Get a json object by `url` and optionally save to db"""
    _json = requests.get(url)
    _json = json.loads(_json.content)

    if not _json or not _json["meals"]:
        return False

    if save_in_db:
        with open("db.json", "r", encoding="utf-8") as file:
            db = json.load(file)
        changed_db = False
        for elem in _json["meals"]:
            if elem not in db:
                db.append(elem)
                changed_db = True
        if changed_db:
            with open("db.json", "w", encoding="utf-8") as file:
                json.dump(db, file, indent=4)

    return _json

@dataclass
class Meal:
    """Represents a JSON object of 'https://www.themealdb.com/'"""
    _id: str
    name: str
    instructions: str
    ingredients: list
    category: str
    tag: str
    area: str
    thumbnail_url: str
    youtube_url: str
    source_url: str
    
    @classmethod
    def from_json(cls, data:dict):
        """Extracts necessary information and returns a Meal object"""
    
        _ingredients = []
        for i in range(1, 100):
            if f"strIngredient{i}" in data and data[f"strIngredient{i}"] not in ["", None]:
                _ingredients.append(
                    (data[f"strIngredient{i}"], data[f"strMeasure{i}"])
                )
    
        return cls(
            _id = data["idMeal"],
            name = data["strMeal"],
            instructions = data["strInstructions"],
            ingredients = _ingredients,
            category = data["strCategory"],
            tag = data["strTags"],
            area = data["strArea"],
            thumbnail_url = data["strMealThumb"],
            youtube_url = data["strYoutube"],
            source_url = data["strSource"]
        )

    def ingredients_translated(self, country_code="de") -> list[str]:
        """Translate ingredients to `country_code`"""
        
        if country_code == "en":
            return self.ingredients

        def conversion(measure:str, old_unit:str, factor:float, new_unit:str):
            """Helper function for unit conversion"""

            if old_unit in measure and "pounded" not in measure:
                measure = measure.split()
                if measure[0].isdecimal():
                    measure[0] = str(int(float(measure[0]) * factor))
                    measure[1] = new_unit

                return " ".join(measure)
            else:
                return measure

        _ingredients = []
        for ing, meas in self.ingredients:
            _meas = meas.lower()
            for elem in ["tsps", "tsp", "teaspoons", "teaspoon"]:
                _meas = _meas.replace(elem, "TL")

            for elem in ["tbsp", "tbs", "tablespoons", "tablespoon"]:
                _meas = _meas.replace(elem, "EL") 

            _meas = conversion(_meas, "oz", 28.3495, "g")
            _meas = conversion(_meas, "pound", 453.592, "g")

            _ingredients.append(
                (ing, _meas)
            )

        return _ingredients

    def instructions_as_md(self) -> str:
        """Returns a markdown representation of the instructions"""

        _instructions = ""
        for i, step in enumerate(self.instructions.split("\r\n"), start=1):
            if step != "":
                if step[0].isdecimal():
                    if step[1].isdecimal():
                        _instructions += f"{i}. {step[2:]} \n "
                    else:
                        _instructions += f"{i}. {step[1:]} \n "
                else:
                    _instructions += f"{i}. {step} \n "

        #return self.instructions.replace("\r\n", "<br>")
        return _instructions