from flask import Flask, render_template

app = Flask(__name__)

@app.route("/plot/")
def plot():
    from pandas_datareader import data
    import yfinance as yf
    import datetime as dt
    from bokeh.plotting import figure,show,output_file
    from bokeh.embed import components
    from bokeh.resources import CDN, INLINE

    yf.pdr_override()

    start = dt.datetime(2019,11,2)
    end = dt.datetime(2020,8,11)
    hours_12 = 12*60*60*1000

    df=data.get_data_yahoo(tickers="TSLA", start=start, end=end)

    def status(open,close):
        if open < close:
            value="Profit"
        elif open > close:
            value="Loss"
        else: value="Equal"
        return value


    df['Status'] = [status(open,close) for open,close in zip(df.Open,df.Close)]
    df['Middle_y'] = (df.Open+df.Close)/2
    df['Height'] = abs(df.Close-df.Open)
    #df

    p = figure(x_axis_type='datetime',width=1000,height=400, title="CandleStick Chart", sizing_mode="scale_width")
    p.grid.grid_line_alpha=0.3

    p.segment(df.index, df.High, df.index, df.Low, color="black")

    p.rect(x=df.index[df.Status =="Profit"],y=df.Middle_y[df.Status=='Profit'], width=hours_12,
           height=df.Height[df.Status=="Profit"],fill_color="#99FF99", line_color="white")

    p.rect(x=df.index[df.Status =="Loss"],y=df.Middle_y[df.Status=='Loss'], width=hours_12,
           height=df.Height[df.Status=="Loss"],fill_color="#CC0000", line_color="white")


    # output_file("cs.html")
    #show(p)

    script1, div1 = components(p)

    cdn_js = CDN.js_files
    cdn_css = CDN.css_files
    return render_template("plot.html", script1=script1, div1=div1, cdn_js=cdn_js[0], cdn_css=cdn_css)

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/about/")
def about():
    return render_template("about.html")


if __name__ == "__main__":
    app.run(debug=True)
