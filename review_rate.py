import openai
import csv
import os

# Set up OpenAI API credentials
openai.api_key = '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'


# Define function to get rating from OpenAI GPT-3 API
def get_rating(review_text):
    prompt = (f"Please score this review on a scale of 1 to 10 based on how satisfied the client is.\n"
              f"Review: {review_text}\n"
              f"Score:")
    response = openai.Completion.create(
        engine="text-davinci-002",
        prompt=prompt,
        max_tokens=1,
        n=1,
        stop=None,
        temperature=0.5,
    )
    score = response.choices[0].text.strip()
    return int(score)


# Define function to analyze reviews in a CSV file
def analyze_reviews(filename):
    # Open CSV file
    with open(filename, "r") as csvfile:
        reader = csv.DictReader(csvfile)
        reviews = []
        for row in reader:
            # Get rating for review text using OpenAI GPT-3 API
            rating = get_rating(row["review text"])
            # Add rating to row dictionary
            row["rating"] = rating
            # Add row to list of reviews
            reviews.append(row)
    # Sort reviews by rating in descending order
    sorted_reviews = sorted(reviews, key=lambda k: k["rating"], reverse=True)
    # Create new filename for analyzed reviews
    base, ext = os.path.splitext(filename)
    new_filename = f"{base}_analyzed{ext}"
    # Open new CSV file for writing
    with open(new_filename, "w", newline="") as csvfile:
        fieldnames = ["email", "review text", "date", "rate", "rating"]
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        # Write header row to CSV file
        writer.writeheader()
        # Write sorted reviews to CSV file
        for row in sorted_reviews:
            writer.writerow(row)


# Call analyze_reviews function for a specific CSV file
analyze_reviews("reviews.csv")
