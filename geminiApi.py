from google import genai
from google.genai import types
import pandas as pd
from datetime import datetime
from colorama import Fore, Style, init

from oeeModels import OEE
from oeeCalculator import calculateOEE

# Set up the client
# Change the API key if the rate  limits are exhausted
try:
    client = genai.Client(
        api_key= "AIzaSyBLFpsx0Ai4YcBTeJsvEQRh8or7eqecCqs"
    )
    chat = client.chats.create(
        model="gemini-2.5-flash"
    )
except Exception as e:
    print(f"{Fore.RED}Error initializing Gemini model: {e}{Style.RESET_ALL}")
    exit()

# Print welcome text
print(f"{Fore.CYAN}{Style.BRIGHT}Welcome to Overall Equipment Effectiveness(OEE) tracking app! {Style.RESET_ALL}")
print(f"{Fore.MAGENTA}Type '{Style.BRIGHT}exit{Style.NORMAL}' or '{Style.BRIGHT}quit{Style.NORMAL}' to end the conversation.{Style.RESET_ALL}")
print(f"{Fore.BLUE}{'-' * 40}{Style.RESET_ALL}")
print(f"{Fore.CYAN}Search for: 'Give me OEE data for device D-3 located in Pune, on July 12th, 2025.'{Style.RESET_ALL}")

# Read the sensors data exxcel sheet
try:
    df = pd.read_excel("sensor_data.xlsx")
    df['Date'] = pd.to_datetime(df['Date'])
except FileNotFoundError:
    print(f"{Fore.RED}Error: File not found.{Style.RESET_ALL}")
    exit()
except Exception as e:
    print(f"{Fore.RED}Error loading or processing: {e}{Style.RESET_ALL}")
    exit()

# Main function to run the chat
while True:
    userInput = input(f"{Fore.YELLOW}You: {Style.RESET_ALL}").strip()

    if userInput.lower() in ["exit", "quit"]:
        print(f"{Fore.CYAN}Exiting chat.{Style.RESET_ALL}")
        break

    if not userInput:
        print("Please enter something to chat.")
        continue

    # intial response from gemini detecting the user's request.
    try:
        intialResponse = chat.send_message(
            message=userInput,
            config={
                "system_instruction": (
                    "You are an intent classifier assistant. Your task is to analyze the user's message and categorize it into one of the following types only:\n"
                    "1. Normal conversation — when the user is having a general chat or casual discussion.\n"
                    "2. Asking for extraction — when the user is requesting specific information to be extracted, analyzed, or processed (e.g., extracting data, summarizing, converting formats, etc.).\n"
                    "Reply with only one of the following two labels based on the user message: 'Normal conversation' or 'Asking for extraction'."
                )
            }
        )

        # Debugging
        # print(f"{Fore.LIGHTBLACK_EX}Intent Classified: {intialResponse.text}{Style.RESET_ALL}")

        final_response = None
        oeeDate: OEE = None

        # Based on the user's response, wether it is normal conversion or wether they are asking for OEE data.
        if(intialResponse.text == "Normal conversation"):
            response = chat.send_message(
                message=userInput,
                config={
                    "system_instruction": "Reply the user in a friendly manner."
                }
            )
            final_response = response.text
        elif(intialResponse.text == "Asking for extraction"):
            response = chat.send_message(
                message=userInput,
                config={
                    "system_instruction": (
                        "Extract the following fields from this user query: Device ID, Location, and Month-Year.\n"
                        "Make sure the reply is the following json format. eg. \n\n"
                        "If the fields are empty, enter default location Banglore and default date: 1-1-2024. Also the deviceId must be: 'D-x'"
                        "{'deviceId': 'D-2', 'location': 'Mumbai', 'day': 4, 'month': 1, 'year': 2024}"
                    ),
                    "response_mime_type": "application/json",
                    "response_schema": OEE,
                }
            )
            final_response =  response.text
            oeeDate: OEE = response.parsed


        # Debugging
        # print(f"{Fore.LIGHTBLACK_EX}{final_response}{Style.RESET_ALL}")    

        # If the user is asking for OEE data, fetch the data from sensors exchel sheet and display it to user using Gemini's prompt. If the device is not found, display similar devices to the user
        if oeeDate:
            oeeCalculation = calculateOEE(df, oeeDate)
            
            # Debugging
            # print(f"{Fore.LIGHTBLACK_EX}{oeeCalculation}{Style.RESET_ALL}")

            reponseToQuery = chat.send_message(
                message= oeeCalculation,
                config= {
                "system_instruction": (
                        "You are a friendly assistance that helps users understand OEE(Overal Equipment Effectiveness). When the user asks for OEE details regarding: \n"
                        "Availability, Performance, Quality and OEE, analyze the query, extract the required details and generate a friendly summary in the following format. \n"
                        "OEE metrics for Device D-3 in Mumbai for April 26, 2024 \n\nAvailability: 83.96% \nPerformance: 99.94% \nQuality: 91.40% \nOverall Equipment Effectiveness (OEE): 76.73%\n\n"
                        "Also include a short summary of the OEE values: \n"
                        "--OEE ≥ 85% → 'This is excellent performance!'\n"
                        "--60% ≤ OEE < 85% → 'This is a good result, but there may be room for improvement.'\n"
                        "--OEE < 60% → 'This indicates a need for improvement.'\n\n"
                        "If no OEE data is found in the query, respond with: 'Did you mean: ' and the list of devices received in query along with thier location and date."
                    )
                }
            )
            final_response = reponseToQuery.text

        if final_response:
            print(f"{Fore.GREEN}Gemini: {Style.RESET_ALL}{final_response}")
        else:
            print("No response was generated.")    

    except Exception as e:
        print(f"{Fore.RED}An error occurred: {e}{Style.RESET_ALL}")



