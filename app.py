from flask import Flask, render_template, request
from eventregistry import EventRegistry, QueryEvents, RequestEventsInfo
import html

app = Flask(__name__)

# Initialize EventRegistry with API key
er = EventRegistry(apiKey="c928102a-30c1-4754-b5a8-b856188bcdd1")

def events_to_html(json_data):
    html_content = '<table border="1"><tr><th>Image</th><th>Event Title</th><th>Date</th><th>Description</th></tr>'
    
    for event in json_data.get('events', {}).get('results', []):
        try:
            title = html.escape(str(event.get('title', 'N/A')))
            date = html.escape(str(event.get('date', 'N/A')))
            description = html.escape(str(event.get('summary', 'N/A')))  # Adjusted to 'summary' for a better description
            image_url = event.get('image', None)  # Assuming 'image' key contains the image URL
            
            if image_url:
                image_tag = f'<img src="{html.escape(image_url)}" width="100"/>'
            else:
                image_tag = "No Image"
            
            html_content += f'<tr><td>{image_tag}</td><td>{title}</td><td>{date}</td><td>{description}</td></tr>'
        
        except Exception as e:
            print(f"Error processing event: {e}")
    
    html_content += '</table>'
    return html_content

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        query = request.form['query']
        
        # Create a query for events
        q = QueryEvents(keywords=query)
        q.setRequestedResult(RequestEventsInfo(sortBy="date", count=50))
        
        # Execute the query and get the results
        events_data = er.execQuery(q)
        
        # Convert JSON to HTML
        html_data = events_to_html(events_data)
        
        return render_template('index.html', html_data=html_data, query=query)
    
    return render_template('index.html')


if __name__ == '__main__':
    app.run(debug=True)
