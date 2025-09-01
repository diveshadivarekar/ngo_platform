from flask import Flask, render_template, abort, request, redirect, url_for, flash, jsonify
import io
import csv
from datetime import datetime

app = Flask(__name__)
# Add a secret key for flashing messages
app.secret_key = 'supersecretkey'

# --- Mock Data ---

announcements_data = [
    {
        'id': 1,
        'title': 'Urgent Need for Blankets in Pune Shelters',
        'content': 'With the recent drop in temperature, our partner shelters in the Pune area are in urgent need of blankets and warm clothing. Donations can be dropped off at any HealthBridge Initiative camp.',
        'author': 'HealthBridge Initiative',
        'category': 'Urgent',
        'timestamp': '2023-11-15 09:30:00'
    },
    {
        'id': 2,
        'title': 'Volunteer Drive for Weekend Tree Planting Event',
        'content': 'Join Green Future Foundation this Saturday for a massive tree planting event in the Aarey Colony area. All tools will be provided. A great opportunity to make a tangible impact!',
        'author': 'Green Future Foundation',
        'category': 'Event',
        'timestamp': '2023-11-14 14:00:00'
    },
    {
        'id': 3,
        'title': 'New Educational Kits Available for Partner NGOs',
        'content': 'Educate For All has developed a new set of science and math educational kits for primary school students. Partner NGOs working in education can request these kits via our resource network page.',
        'author': 'Educate For All',
        'category': 'Information',
        'timestamp': '2023-11-12 11:00:00'
    }
]


ngo_impact_data = [
    {
        'id': 1,
        'slug': 'green-future-foundation',
        'name': 'Green Future Foundation',
        'area': 'Environmental Conservation',
        'location': {'lat': 19.0760, 'lon': 72.8777}, # Mumbai coordinates
        'start_date': '2022-01-15',
        'impact': {
            'Trees Planted': 12500,
            'Regions Covered': 'North Mumbai, Western Suburbs',
            'CO2 Reduced (Tonnes)': 500
        },
        'details': 'Focused on reforestation and urban greening projects, the Green Future Foundation has been instrumental in combating air pollution across Mumbai. They also conduct workshops in schools to promote environmental awareness.',
        'goal': {'metric': 'Trees Planted', 'target': 20000},
        'sdg': [13, 15], # Climate Action, Life on Land
        'resources_available': [
            {'name': 'Gardening Tools', 'type': 'Goods', 'quantity': '50 sets', 'sdg': [15]},
            {'name': 'Environmental Education Kits', 'type': 'Goods', 'quantity': '200 kits', 'sdg': [4, 13]}
        ],
        'resources_needed': [
            {'name': 'Volunteers for Tree Planting', 'type': 'Volunteers', 'quantity': '100 hours/month', 'sdg': [13, 15], 'urgency': 'High'},
            {'name': 'Sapling Donations', 'type': 'Goods', 'quantity': '5000 saplings', 'sdg': [15], 'urgency': 'Medium'}
        ]
    },
    {
        'id': 2,
        'slug': 'educate-for-all',
        'name': 'Educate For All',
        'area': 'Children\'s Education',
        'location': {'lat': 18.5204, 'lon': 73.8567}, # Pune coordinates
        'start_date': '2023-06-20',
        'impact': {
            'Students Enrolled': 780,
            'Schools Supported': 15,
            'Literacy Rate Improvement (%)': 12
        },
        'details': 'Educate For All provides underprivileged children with access to quality education, school supplies, and mid-day meals. Their volunteer-led tutoring programs have shown remarkable success.',
        'goal': {'metric': 'Students Enrolled', 'target': 1000},
        'sdg': [4], # Quality Education
        'resources_available': [
            {'name': 'Volunteer Tutors (Math & Science)', 'type': 'Volunteers', 'quantity': '20 volunteers', 'sdg': [4]},
            {'name': 'Used Laptops for Students', 'type': 'Goods', 'quantity': '25 units', 'sdg': [4, 10]}
        ],
        'resources_needed': [
            {'name': 'Stationery Kits', 'type': 'Goods', 'quantity': '500 kits', 'sdg': [4], 'urgency': 'High'},
            {'name': 'Digital Classroom Projector', 'type': 'Goods', 'quantity': '1 unit', 'sdg': [4], 'urgency': 'Low'}
        ]
    },
    {
        'id': 3,
        'slug': 'healthbridge-initiative',
        'name': 'HealthBridge Initiative',
        'area': 'Community Health',
        'location': {'lat': 19.2183, 'lon': 72.9781}, # Thane coordinates
        'start_date': '2022-11-01',
        'impact': {
            'Medical Camps Held': 52,
            'Patients Treated': 21000,
            'Vaccinations Administered': 15000
        },
        'details': 'This initiative runs mobile medical camps in remote and underserved areas, providing free check-ups, essential medicines, and critical vaccinations to vulnerable populations.',
        'goal': {'metric': 'Patients Treated', 'target': 25000},
        'sdg': [3], # Good Health and Well-being
        'resources_available': [
            {'name': 'Mobile Medical Van', 'type': 'Services', 'quantity': '1 van', 'sdg': [3]},
            {'name': 'General Physicians (Volunteer)', 'type': 'Volunteers', 'quantity': '5 doctors', 'sdg': [3]}
        ],
        'resources_needed': [
            {'name': 'Basic Medical Supplies', 'type': 'Goods', 'quantity': 'Urgent resupply needed', 'sdg': [3], 'urgency': 'High'},
        ]
    },
    {
        'id': 4,
        'slug': 'safe-haven-animal-rescue',
        'name': 'Safe Haven Animal Rescue',
        'area': 'Animal Welfare',
        'location': {'lat': 19.0213, 'lon': 72.8562}, # South Mumbai
        'start_date': '2023-02-10',
        'impact': {
            'Animals Rescued': 450,
            'Successful Adoptions': 320,
            'Community Awareness Programs': 25
        },
        'details': 'Dedicated to rescuing and rehabilitating stray animals, Safe Haven also runs adoption drives and awareness campaigns to promote responsible pet ownership and compassion for all animals.',
        'goal': {'metric': 'Successful Adoptions', 'target': 400},
        'sdg': [15], # Life on Land
         'resources_available': [],
        'resources_needed': [
            {'name': 'Foster Homes for Animals', 'type': 'Volunteers', 'quantity': '20 homes', 'sdg': [15], 'urgency': 'Medium'},
            {'name': 'Animal Food (Bulk)', 'type': 'Goods', 'quantity': '500 kg', 'sdg': [15, 2], 'urgency': 'High'}
        ]
    }
]

SDG_TITLES = {
    1: "No Poverty", 2: "Zero Hunger", 3: "Good Health and Well-being", 4: "Quality Education",
    5: "Gender Equality", 6: "Clean Water and Sanitation", 7: "Affordable and Clean Energy",
    8: "Decent Work and Economic Growth", 9: "Industry, Innovation and Infrastructure",
    10: "Reduced Inequality", 11: "Sustainable Cities and Communities",
    12: "Responsible Consumption and Production", 13: "Climate Action", 14: "Life Below Water",
    15: "Life on Land", 16: "Peace and Justice Strong Institutions", 17: "Partnerships to achieve the Goal"
}

SDG_COLORS = {
    1: "E5243B", 2: "DDA63A", 3: "4C9F38", 4: "C5192D", 5: "FF3A21",
    6: "26BDE2", 7: "FCC30B", 8: "A21942", 9: "FD6925", 10: "DD1367",
    11: "FD9D24", 12: "BF8B2E", 13: "3F7E44", 14: "0A97D9", 15: "56C02B",
    16: "00689D", 17: "19486A"
}

@app.context_processor
def inject_sdg_data():
    """Make SDG data available to all templates."""
    return dict(sdg_titles=SDG_TITLES, sdg_colors=SDG_COLORS)

# --- Routes ---

@app.route('/')
def home():
    """Main home page."""
    return render_template('index.html')

@app.route('/dashboard')
def dashboard():
    """Impact Measurement Dashboard page."""
    year_filter = request.args.get('year', 'all')
    area_filter = request.args.get('area', 'all')

    filtered_ngos = ngo_impact_data

    # Filter by year
    if year_filter != 'all':
        filtered_ngos = [ngo for ngo in filtered_ngos if datetime.strptime(ngo['start_date'], '%Y-%m-%d').year == int(year_filter)]
    
    # Filter by area
    if area_filter != 'all':
        filtered_ngos = [ngo for ngo in filtered_ngos if ngo['area'] == area_filter]

    # Get unique years and areas for filter dropdowns
    unique_years = sorted(list(set(datetime.strptime(n['start_date'], '%Y-%m-%d').year for n in ngo_impact_data)), reverse=True)
    unique_areas = sorted(list(set(n['area'] for n in ngo_impact_data)))

    return render_template('dashboard.html', 
                           ngos=filtered_ngos, 
                           unique_years=unique_years, 
                           unique_areas=unique_areas,
                           selected_year=year_filter,
                           selected_area=area_filter)


@app.route('/ngo/<slug>')
def ngo_profile(slug):
    """Detailed profile page for a single NGO."""
    ngo = next((ngo for ngo in ngo_impact_data if ngo['slug'] == slug), None)
    if ngo is None:
        abort(404)
    return render_template('ngo_profile.html', ngo=ngo)

@app.route('/export-csv')
def export_csv():
    """Exports the NGO impact data as a CSV file."""
    output = io.StringIO()
    writer = csv.writer(output)
    
    # Write header
    writer.writerow(['NGO Name', 'Area of Impact', 'Start Date', 'Metric', 'Value'])
    
    # Write data
    for ngo in ngo_impact_data:
        for metric, value in ngo['impact'].items():
            writer.writerow([ngo['name'], ngo['area'], ngo['start_date'], metric, value])
            
    output.seek(0)
    
    return (output.getvalue(), 200, {
        'Content-Disposition': 'attachment; filename="ngo_impact_report.csv"',
        'Content-Type': 'text/csv'
    })

@app.route('/resources')
def resource_network():
    """Community Resource Sharing Network page."""
    type_filter = request.args.get('type', 'all')
    sdg_filter = request.args.get('sdg', 'all')

    # Flatten all resources for filtering and display
    all_needed = []
    all_available = []
    unique_types = set()
    unique_sdgs = set()

    for ngo in ngo_impact_data:
        if ngo.get('resources_needed'):
            for res in ngo['resources_needed']:
                all_needed.append({'ngo': ngo, 'resource': res})
                unique_types.add(res['type'])
                for s in res['sdg']:
                    unique_sdgs.add(s)

        if ngo.get('resources_available'):
            for res in ngo['resources_available']:
                all_available.append({'ngo': ngo, 'resource': res})
                unique_types.add(res['type'])
                for s in res['sdg']:
                    unique_sdgs.add(s)
    
    # Apply filters
    if type_filter != 'all':
        all_needed = [item for item in all_needed if item['resource']['type'] == type_filter]
        all_available = [item for item in all_available if item['resource']['type'] == type_filter]

    if sdg_filter != 'all':
        sdg_filter_int = int(sdg_filter)
        all_needed = [item for item in all_needed if sdg_filter_int in item['resource']['sdg']]
        all_available = [item for item in all_available if sdg_filter_int in item['resource']['sdg']]

    return render_template('resources.html', 
                           ngos=ngo_impact_data,
                           unique_types=sorted(list(unique_types)),
                           unique_sdgs=sorted(list(unique_sdgs)),
                           selected_type=type_filter,
                           selected_sdg=sdg_filter)

@app.route('/request-resource')
def request_resource():
    """Handles a resource request."""
    ngo_id = request.args.get('ngo_id')
    resource_name = request.args.get('resource_name')
    flash(f"Your request for '{resource_name}' has been sent to the providing NGO. They will contact you shortly.", 'success')
    return redirect(url_for('resource_network'))

@app.route('/donate', methods=['GET', 'POST'])
def donate_resource():
    """Displays and handles the donation form."""
    if request.method == 'POST':
        # In a real app, you'd save this to a database
        donor_name = request.form.get('donor_name')
        flash(f"Thank you, {donor_name}! Your donation offer has been received and will be reviewed by an administrator.", 'success')
        return redirect(url_for('resource_network'))
    
    # For GET request, render the separate donation page
    return render_template('donate.html')

@app.route('/data-collection', methods=['GET', 'POST'])
def data_collection():
    """Displays and handles the field data collection form."""
    if request.method == 'POST':
        ngo_id = int(request.form.get('ngo_id'))
        
        # Check if we are updating an existing metric or adding a new one
        metric_choice = request.form.get('metric_choice')
        if metric_choice == 'new':
            metric_name = request.form.get('new_metric_name')
        else:
            metric_name = metric_choice

        metric_value = request.form.get('metric_value')
        
        ngo_to_update = next((ngo for ngo in ngo_impact_data if ngo['id'] == ngo_id), None)
        
        if ngo_to_update and metric_name:
            current_value = ngo_to_update['impact'].get(metric_name, 0)
            try:
                new_value = float(metric_value)
                if new_value.is_integer():
                    new_value = int(new_value)
                
                if isinstance(current_value, (int, float)):
                    ngo_to_update['impact'][metric_name] = current_value + new_value
                else:
                    ngo_to_update['impact'][metric_name] = new_value
                
                flash(f"Data for '{metric_name}' submitted successfully for {ngo_to_update['name']}!", 'success')
            except (ValueError, TypeError):
                flash(f"Invalid value '{metric_value}'. Please enter a number.", 'error')
        else:
            flash("Could not submit data. Please ensure all fields are correct.", 'error')
        
        return redirect(url_for('data_collection'))

    return render_template('data_collection.html', ngos=ngo_impact_data)

@app.route('/api/ngo-metrics/<int:ngo_id>')
def get_ngo_metrics(ngo_id):
    """API endpoint to get existing metrics for a given NGO."""
    ngo = next((n for n in ngo_impact_data if n['id'] == ngo_id), None)
    if ngo:
        # Return only metrics that have a numeric value
        numeric_metrics = {k: v for k, v in ngo['impact'].items() if isinstance(v, (int, float))}
        return jsonify(list(numeric_metrics.keys()))
    return jsonify([])

@app.route('/announcements', methods=['GET', 'POST'])
def announcements():
    """Displays and handles announcements."""
    if request.method == 'POST':
        new_announcement = {
            'id': len(announcements_data) + 1,
            'title': request.form.get('title'),
            'content': request.form.get('content'),
            'author': request.form.get('author'),
            'category': request.form.get('category'),
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        }
        announcements_data.insert(0, new_announcement) # Add to the top of the list
        flash('Your announcement has been posted!', 'success')
        return redirect(url_for('announcements'))

    # Sort announcements by timestamp for display
    sorted_announcements = sorted(announcements_data, key=lambda x: x['timestamp'], reverse=True)
    return render_template('announcements.html', announcements=sorted_announcements, ngos=ngo_impact_data)


# --- Error Handler ---
@app.errorhandler(404)
def page_not_found(e):
    """Custom 404 error page."""
    return render_template('404.html'), 404

if __name__ == '__main__':
    app.run(debug=True)

