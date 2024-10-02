import dynamodb
import boto3
import streamlit as st
import pandas as pd
#from datetime import datetime
import  datetime
from ast import main

st.title("Dagbok")

table = dynamodb.Table("inlagg")


st.header("Skriv ett nytt inlägg")
date = st.date_input("Datum", datetime.datetime.now())
text = st.text_area("Inlägg", height=200)

today = datetime.datetime.today()
week_num = today.isocalendar()[1]
st.write ("Vecka:", week_num,"")


AWS_REGION ="us-east-1"

dynamodb = boto3.resource('dynamodb', region_name=AWS_REGION)


def add_entry(date, text, today):
    table.put_item(
        Item={
            'date': date,
            'text': text,
            'today': today,
        }
    )

def get_entries_by_week(week):
   response = table.scan(
       FilterExpression=boto3.dynamodb.conditions.Attr('week').eq(week)
   )
   return response['Items']

allowed_weeks = [str(week) for week in range(38,50) if week !=44]
selected_week = st.selectbox("Välj vecka att visa",allowed_weeks)

items = get_entries_by_week(int(selected_week))

if not items:
    st.info(f"Inga inlägg hittades för vecka {selected_week}.")
else:
      for item in items:
        st.write(f"**date:** {item['datum']}")
        st.write(f"**text:** {item['text']}")
        st.write(f"**'today:'**{item['today']}")



if st.button("Spara inlägg"):
    add_entry(date, text, today)
    st.success("Inlägget har sparats!")



st.header("Tidigare inlägg")
if st.session_state.entries:
    for entry in st.session_state.entries:
        st.subheader(entry["date"].strftime("%Y-%m-%d"))
        st.subheader(entry["today"])
        st.write(entry["text"])
        st.markdown("---")
else:
    st.write("Inga inlägg än.")

if st.button("Rensa alla inlägg"):
    st.session_state.entries = []
    st.success("Alla inlägg har rensats!")

st.sidebar.title("Inställningar")
st.sidebar.write("Justera dina inställningar här.")

if __name__ == "__main__":
   main()
