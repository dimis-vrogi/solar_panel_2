import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier
import random
import streamlit as st

st.title("Εφαρμογή Φωτοβολταϊκού")


@st.cache_resource
def load_data_and_train_model():
    real_data = [
    # hour, weather, panel_area, temp, season, use_tracker
    [8,0,0.1,18,2,1],
    [9,0,0.1,20,2,1],
    [10,0,0.1,22,2,1],
    [11,0,0.2,25,2,1],
    [12,0,0.2,28,3,1],
    [13,0,0.3,30,3,1],
    [14,1,0.3,29,3,1],
    [15,1,0.2,27,3,1],
    [16,1,0.2,25,3,0],
    [17,2,0.1,22,4,0],
    [18,2,0.1,20,4,0],
    [19,2,0.1,18,4,0],
    [20,3,0.1,16,4,0],
    [21,3,0.1,15,4,0],
    [6,2,0.05,12,1,0],
    [7,1,0.05,14,1,0],
    [10,2,0.2,19,2,0],
    [12,2,0.3,21,2,0],
    [14,1,0.3,24,2,1],
    [16,1,0.2,23,2,0],
    ]

    synthetic_data = []

    for _ in range(300):
        hour = random.randint(0,23)
        weather = random.randint(0,3)
        panel_area = random.choice([0.5,10,20,50,100])
        temp = random.randint(0,40)
        season = random.randint(1,4)

        if (hour < 6 or hour > 21) and season!=1 :
            use_tracker = 0
        elif season == 1 and (hour < 6 or hour>19):
            use_tracker = 0
        elif weather >= 2:
            use_tracker = 0
        elif panel_area < 5 and weather != 1:
            use_tracker = 0
        elif panel_area < 5 and (hour<12 or hour>16):
            use_tracker = 0
        elif temp<-5:
            use_tracker = 0
        else:
            use_tracker = 1

        synthetic_data.append([hour,weather,panel_area,temp,season,use_tracker])

    columns = ["hour","weather","panel_area","temperature","season","use_tracker"]
    df = pd.DataFrame(real_data + synthetic_data, columns=columns)


    X = df[["hour","weather","panel_area","temperature","season"]]
    y = df["use_tracker"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2)

    model = DecisionTreeClassifier(max_depth=6)
    model.fit(X_train, y_train)
    
    st.write(f"Ακρίβεια μοντέλου: {model.score(X_test, y_test):.2f}")
    return model

model = load_data_and_train_model()


st.sidebar.header("Δώσε συνθήκες:")

hour = st.sidebar.slider("Ώρα (0-23): ",0,23, 12)
weather_options = {
    "Καθαρός": 0,
    "Μερική συννεφιά": 1,
    "Πολλή συννεφιά": 2,
    "Βροχή": 3
}
selected_weather = st.sidebar.selectbox("Καιρός: ", list(weather_options.keys()))
weather = weather_options[selected_weather]

panel_area = st.sidebar.number_input("Επιφάνεια πάνελ (0.5-100 m²): ", min_value=0.5, max_value=100.0, value=10.0, step=0.1)
temperature = st.sidebar.slider("Θερμοκρασία (-20 έως 60°C): ",-20,60, 20)
season_options = {
    "Χειμώνας": 1,
    "Άνοιξη": 2,
    "Καλοκαίρι": 3,
    "Φθινόπωρο": 4
}
selected_season = st.sidebar.selectbox("Εποχή: ", list(season_options.keys()))
season = season_options[selected_season]


if st.sidebar.button("Πρόβλεψη"): 
    prediction = model.predict([[hour,weather,panel_area,temperature,season]])


    if prediction[0] == 1:
        st.success("Συμφέρει η χρήση του solar tracker")
    else:
        st.warning("Δεν συμφέρει η χρήση του solar tracker")
