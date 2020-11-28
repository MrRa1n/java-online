from javaonline import app, read_config, configure_logger

print(app.url_map)

if __name__ == '__main__':
    read_config(app)
    configure_logger(app)
    app.run(debug=True, use_reloader=False)