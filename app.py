from flask import Flask, render_template, request
from eventregistry import EventRegistry, QueryEvents, RequestEventsInfo, ReturnInfo, EventInfoFlags
import html
from datetime import datetime

app = Flask(__name__)

# Initialize EventRegistry with API key
er = EventRegistry(apiKey="c928102a-30c1-4754-b5a8-b856188bcdd1")

def events_to_html(json_data):
    # Start the HTML content with a styled table
    html_content = '''
    <style>
        table {
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
            font-size: 18px;
            text-align: left;
        }
        th, td {
            padding: 12px;
            border-bottom: 1px solid #ddd;
        }
        th {
            background-color: #4CAF50;
            color: white;
        }
        tr:nth-child(even) {
            background-color: #f2f2f2;
        }
        tr:hover {
            background-color: #ddd;
        }
        img {
            max-width: 100px;
            height: auto;
        }
    </style>
    <table>
        <tr>
            <th>Image</th>
            <th>Event Title</th>
            <th>Date</th>
            <th>Description</th>
            <th>Timestamp</th>
        </tr>
    '''
    
    for event in json_data.get('events', {}).get('results', []):
        try:
            title = html.escape(str(event.get('title', 'N/A')))
            date = html.escape(str(event.get('eventDate', 'N/A')))
            description = html.escape(str(event.get('summary', 'N/A')))
            image_url = event.get('eventImage', {}).get('url', None)
            
            # Get timestamp
            timestamp = event.get('dateTime')
            if timestamp:
                timestamp = datetime.fromisoformat(timestamp).strftime('%Y-%m-%d %H:%M:%S')
            else:
                timestamp = 'N/A'
            
            if image_url:
                image_tag = f'<img src="{html.escape(image_url)}" width="100"/>'
            else:
                image_tag = "No Image"
            
            html_content += f'''
            <tr>
                <td>{image_tag}</td>
                <td>{title}</td>
                <td>{date}</td>
                <td>{description}</td>
                <td>{timestamp}</td>
            </tr>
            '''
            
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
        q.setRequestedResult(RequestEventsInfo(
            sortBy="date", 
            count=50,
            returnInfo = ReturnInfo(
                eventInfo = EventInfoFlags(
                    title=True, 
                    summary=True, 
                    eventDate=True, 
                    eventImage=True,
                    dateTime=True
                )
            )
        ))
        
        # Execute the query and get the results
        events_data = er.execQuery(q)
        
        # Convert JSON to HTML
        html_data = events_to_html(events_data)
        
        return render_template('index.html', html_data=html_data, query=query)
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)