from flask import Flask, request, jsonify, render_template
from groq import Groq

app = Flask(__name__)

# Initialize the Groq client
client = Groq(api_key="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")


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/get_suggestions', methods=['POST'])
def get_suggestions():
    try:
        data = request.json
        relationship = data.get("relationship", "").strip()

        if not relationship:
            return jsonify({"error": "Relationship input is required"}), 400

        prompts = [
            f"give me something cool to do for my {relationship} I like in one line",
            f"give me something cool to gift for my {relationship} I like in one line",
            f"give me something cool to say to my {relationship} I like in one line"
        ]

        results = []
        for prompt in prompts:
            completion = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=[{"role": "user", "content": prompt}],
                temperature=1,
                max_tokens=1024,
                top_p=1,
                stream=False,
            )
            # Adjust this line based on the Groq response structure
            results.append(completion.choices[0].message.content)

        return jsonify({"suggestions": results})
    except Exception as e:
        print(f"Error occurred: {e}")
        return jsonify({"error": "An unexpected error occurred"}), 500


@app.route('/test_groq')
def test_groq():
    try:
        test_prompt = "give me something cool to say to my friend"
        completion = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[{"role": "user", "content": test_prompt}],
            temperature=1,
            max_tokens=1024,
            top_p=1,
            stream=False,
        )
        # Adjust this line based on the Groq response structure
        result = completion.choices[0].message.content
        return jsonify({"test_response": result})
    except Exception as e:
        print(f"Groq API Test Error: {e}")
        return jsonify({"error": "Groq API test failed"}), 500



if __name__ == '__main__':
    app.run(debug=True)
