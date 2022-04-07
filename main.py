import config
import requests
import datetime as dt

GENDER = config.MY_GENDER
AGE = config.MY_AGE
WEIGHT_KG = config.MY_WEIGHT_KG
HEIGHT_CM = config.MY_HEIGHT_CM

SHEETY_API_KEY = config.SHEETY_API_KEY

current_date = dt.date.today().strftime("%m/%d/%Y")
current_time = dt.datetime.now().strftime("%I:%M:%S")


nutrition_url = "https://trackapi.nutritionix.com"
nutrition_exercise_endpoint = f"{nutrition_url}/v2/natural/exercise"
nutrition_header = {
    "x-app-id": config.NUTRITION_APP_ID,
    "x-app-key": config.NUTRITION_APP_KEY,

}
query_question = input("What exercise did you do today? ")
exercise_params = {
    "query": query_question,
    "gender": GENDER,
    "weight_kg": WEIGHT_KG,
    "height_cm": HEIGHT_CM,
    "age": AGE
}

nutrition_request = requests.post(url=nutrition_exercise_endpoint, json=exercise_params, headers=nutrition_header)
nutrition_data = nutrition_request.json()
workout_url = f"https://api.sheety.co/{SHEETY_API_KEY}/workoutMaster/workouts"

for exercise_data in nutrition_data["exercises"]:
    g_sheets_row_instance = {
        "workout":
            {
                "date": current_date,
                "time": current_time,
                "exercise": exercise_data["name"],
                "duration": exercise_data["duration_min"],
                "calories": exercise_data["nf_calories"],
            }
        }

    post_exercise_data = requests.post(url=workout_url, json=g_sheets_row_instance, headers=config.AUTH_HEADER)


print("Finished Updating")



