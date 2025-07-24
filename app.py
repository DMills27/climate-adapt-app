from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'secret123'  # Needed for flash messages

@app.route('/', methods=['GET', 'POST'])
def user_form():
    if request.method == 'POST':
        form_data = {
            'country': request.form.get('country'),
            'region': request.form.get('region'),
            'coordinates': request.form.get('coordinates'),
            'space_type': request.form.get('space_type'),
            'area': request.form.get('area'),
            'water': request.form.get('water'),
            'electricity': request.form.get('electricity'),
            'traditions': request.form.get('traditions')
        }
        print("Received form data:", form_data)
        flash("Form submitted successfully!", "success")
        return redirect(url_for('user_form'))

    countries = ['United Arab Emirates', 'India', 'Kenya', 'Brazil', 'USA', 'Other']
    return render_template('form.html', countries=countries)

if __name__ == '__main__':
    app.run(debug=True)
