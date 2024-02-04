
#--web true

def main(args):
    return {"body": {"output": generate_html_from_json(args.get('events'))}}

def generate_html_from_json(json_response):
    if not json_response:
        return "<html><body><h2>No calendar events available</h2></body></html>"

    html = """
    <html>
    <body>
        <h2>Calendar Events</h2>
        <table border="1">
            <tr>
                <th>Start</th>
                <th>End</th>
                <th>Organizer</th>
                <th>Summary</th>
            </tr>
    """

    for event in json_response:
        html += f"""
            <tr>
                <td>{event['start']}</td>
                <td>{event['end']}</td>
                <td>{event['organizer']}</td>
                <td>{event['summary']}</td>
            </tr>
        """

    html += """
        </table>
    </body>
    </html>
    """

    return html

events_data = []

html_output = generate_html_from_json(events_data)
