import matplotlib.pyplot as plt
import time
import flask
from Capstone_Functions import calc_splits, splits_in_seconds, get_scatter
from flask import Flask, render_template, request

app = Flask(__name__)
app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0

# Initial page when loading web app
@app.route('/')
def index():
    return flask.render_template('index.html')

# Login page that validates for 'admin' in Username and Password fields
@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] != 'admin' and request.form['password'] != 'admin':
            error = 'Please enter a valid Username and Password.'
        else:
            return render_template('enter_time.html')
    return render_template('login.html', error=error)

# Page where user will enter their desired finish time
@app.route('/enter_time', methods=['POST'])
def enter_time():
    return flask.render_template('enter_time.html')

# Page that displays table and two graphs for predicted race splits
@app.route('/predict', methods=['POST'])
def predict():
    # Get values entered by user
    if request.method == 'POST':
        to_predict_list = request.form.to_dict()
        to_predict_list = list(to_predict_list.values())
        to_predict_list = list(map(float, to_predict_list))
    # Store values in separate variables
    finish_hr = to_predict_list[0]
    finish_min = to_predict_list[1]
    finish_sec = to_predict_list[2]

    # Convert input to seconds
    input_in_seconds = finish_hr * 3600 + finish_min * 60 + finish_sec
    my_array = []
    my_array = calc_splits(input_in_seconds)
    splits_list = splits_in_seconds(input_in_seconds)
    array_base = [['5k', '10k', '15k', '20k', 'Half', '25k', '30k', '35k', '40k', 'Final', 'Avg Mile Pace'],
                  [1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11]]
    # Set the final array position to the average pace per mile of the desired finish time
    array_base[1][10] = time.strftime('%H:%M:%S', time.gmtime(round(input_in_seconds / 26.2)))

    array_line_graph = [['5k', '10k', '15k', '20k', 'Half', '25k', '30k', '35k', '40k', 'Final'],
                        splits_list]

    i = -1
    while i < 9:
        i += 1
        array_base[1][i] = my_array[i]

    prediction = array_base

    filename = "static/pace_graph.png"

    # Checks for existence of line graph file, if exists, replaces the file with the line graph
    fig = plt.figure()
    if fig.get_axes():
        plt.clf()
        plt.plot(array_line_graph.__getitem__(0), array_line_graph.__getitem__(1), label='Predicted Splits')
        # added line to show if ran a consistent pace
        plt.plot(['5k', 'Final'], [((input_in_seconds/26.2) * 3.10686), input_in_seconds], label='Avg Pace')
        plt.xlabel('distance')
        plt.ylabel('time in seconds')
        plt.title('Predicted Splits vs. Avg Pace per Mile')
        plt.legend()
        plt.savefig(filename)
    else:
        plt.plot(array_line_graph.__getitem__(0), array_line_graph.__getitem__(1), label='Predicted Splits')
        # added line to show if ran a consistent pace
        plt.plot(['5k', 'Final'], [((input_in_seconds / 26.2) * 3.10686), input_in_seconds], label='Avg Pace')
        plt.xlabel('distance')
        plt.ylabel('time in seconds')
        plt.title('Predicted Splits vs. Avg Pace per Mile')
        plt.legend()
        plt.savefig(filename)

    plt.close(filename)

    scatter_file = "static/pace_scatter.png"
    scatter_fig = plt.figure()
    # Checks for existence of scatter plot graph file, if exists, replaces the file with the scatter plot
    if scatter_fig.get_axes():
        plt.clf()

        x = ['5k', '10k', '15k', '20k', 'Half', '25k', '30k', '35k', '40k', 'Final']
        y = get_scatter(input_in_seconds)

        for split_dist, split_time in zip(x, y):
            plt.scatter([split_dist] * len(split_time), split_time)

        plt.plot(x, splits_list, 'o-', label='Predicted Splits')
        plt.legend()
        plt.title('Predicted Splits vs. Previous Runners\' Times')
        plt.savefig(scatter_file)
    else:
        x = ['5k', '10k', '15k', '20k', 'Half', '25k', '30k', '35k', '40k', 'Final']
        y = get_scatter(input_in_seconds)

        for split_dist, split_time in zip(x, y):
            plt.scatter([split_dist] * len(split_time), split_time)

        plt.plot(x, splits_list, 'o-', label='Predicted Splits')
        plt.legend()
        plt.title('Predicted Splits vs. Previous Runners\' Times')
        plt.savefig(scatter_file)

    plt.close(scatter_file)

    return render_template('predict.html', filename=filename, prediction=prediction, scatter_file=scatter_file)


if __name__ == '__main__':
    app.run(debug=True)
