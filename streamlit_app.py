import disease_detection

app = disease_detection.create_app()
app.run(debug=True)