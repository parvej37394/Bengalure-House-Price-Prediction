import pickle
import pandas as pd
from flask import Flask, render_template, request
import plotly.express as px
import plotly.io as pio

app = Flask(__name__)

# ডাটা এবং মডেল লোড
data = pd.read_csv("Cleaned_data.csv")
pipe = pickle.load(open("rig.pkl", "rb"))

def generate_3d_chart():
    # র্যান্ডম ৫০০টি ডেটা পয়েন্ট নেওয়া (দ্রুত লোড হওয়ার জন্য)
    sample_df = data.sample(min(600, len(data)), random_state=42)

    # আপগ্রেডেড ও কালারফুল ৩D Scatter Plot
    fig = px.scatter_3d(
        sample_df,
        x='total_sqft',
        y='bhk',
        z='price',
        color='price',  # দাম অনুযায়ী কালার শেড পরিবর্তন হবে
        size='bath',    # বাথরুম সংখ্যা অনুযায়ী পয়েন্টের আকার বড়/ছোট হবে
        color_continuous_scale='Turbo',  # আকর্ষণীয় ও উজ্জ্বল কালার প্যালেট (Turbo/Plasma/Viridis)
        hover_name='location',  # মাউস নিলে উপরে লোকেশন নাম দেখাবে
        labels={
            'total_sqft': 'Total SqFt',
            'bhk': 'BHK (Bedrooms)',
            'price': 'Price (Lakhs ₹)',
            'bath': 'Bathrooms'
        },
        title="<b>3D Market Explorer: SqFt vs BHK vs Price</b>"
    )

    # Hover-এ মাউস আনলে কী কী তথ্য দেখাবে তার কাস্টম ফরম্যাট
    fig.update_traces(
        hovertemplate="<b>Location:</b> %{hovertext}<br>" +
                      "<b>Area:</b> %{x} sqft<br>" +
                      "<b>BHK:</b> %{y}<br>" +
                      "<b>Price:</b> ₹%{z} Lakhs<br>" +
                      "<extra></extra>",
        marker=dict(opacity=0.85, line=dict(width=0.5, color='DarkSlateGrey'))
    )

    # থিম এবং ৩D গ্রিডের কাস্টমাইজেশন
    fig.update_layout(
        template="plotly_dark",  # ডার্ক মোড লুকের জন্য
        paper_bgcolor="rgba(0,0,0,0)",  # কার্ডের সাথে ব্যাকগ্রাউন্ড মিলিয়ে নেওয়া
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(l=10, r=10, b=10, t=50),
        font=dict(family="Segoe UI, sans-serif", size=12, color="#ffffff"),
        scene=dict(
            xaxis=dict(backgroundcolor="#1e1e2f", gridcolor="#444466", title="SqFt"),
            yaxis=dict(backgroundcolor="#1e1e2f", gridcolor="#444466", title="BHK"),
            zaxis=dict(backgroundcolor="#1e1e2f", gridcolor="#444466", title="Price (Lakhs)"),
            camera=dict(
                eye=dict(x=1.5, y=1.5, z=1.2)  # ৩D ক্যানভাসের ভিউ অ্যাঙ্গেল
            )
        )
    )

    return pio.to_html(fig, full_html=False, config={'responsive': True})


@app.route('/')
def index():
    locations = sorted(data['location'].unique())
    graph_html = generate_3d_chart()
    return render_template('index.html', locations=locations, graph_html=graph_html)


@app.route('/predict', methods=['POST'])
def predict():
    location = request.form.get('location')
    bhk = int(request.form.get('bhk'))
    bath = float(request.form.get('bath'))
    total_sqft = float(request.form.get('total_sqft'))

    input_data = pd.DataFrame([[location, total_sqft, bath, bhk]], 
                              columns=['location', 'total_sqft', 'bath', 'bhk'])

    prediction = pipe.predict(input_data)[0]
    output = round(prediction, 2)

    locations = sorted(data['location'].unique())
    graph_html = generate_3d_chart()

    return render_template('index.html', locations=locations, prediction=f"₹ {output} Lakhs", graph_html=graph_html)

if __name__ == '__main__':
    app.run(debug=True, port=5001)