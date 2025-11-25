const ids = [
    "7990e121-9aeb-4d80-8318-0eea4fa07cd5",
    "61fade10-a3b7-4b57-bd1f-4ba96c255ce9",
    "26b0eb0e-e14e-4ba6-a333-ab822dccce4e",
    "33f89376-2f1e-4975-846e-add002508888",
    "dbdb5234-bdb4-4ec6-849c-e726e15473f4"

]

function generateStatTiles(ids){
    let container = document.querySelector(".stat-container")

    for(let i = 0; i<ids.length; i++){
        container.insertAdjacentHTML("beforeend",
            `<iframe 
                class="stat-frame"
                src="https://charts.mongodb.com/charts-project-0-btywdyw/embed/charts?id=${ids[i]}&maxDataAge=14400&theme=dark&attribution=false">
            </iframe>`
        )
        console.log("Appended: " + ids[i])
    }
}

document.addEventListener("DOMContentLoaded", (event) => {
    generateStatTiles(ids);
});


/**
 * PlotCard for Barcharts
 * The plot can be partly styled via css using the .plot-card selector
 * 
 */
class PlotCardBar {
    /**
     * Creates a new PlotCard with the given options
     * Options must contain:
     * data -> a list of Traces with name, labels, values and optionally a color
     * Options may contain:
     * color, title, orientaion
     * 
     * @param {String} plotName 
     * @param {Object} options 
     */
    constructor(plotName, options) {

        this.plotName = plotName;
        this.data = options.data;
        this.orientation = options.orientation ?? "v";

        this.layout = {
            title: options.title,
            barmode: 'stack',
            plot_bgcolor: options.color ?? "rgb(38, 39, 43)",
            paper_bgcolor: options.color ?? "rgb(38, 39, 43)",
            font: {
                family: 'Arial',
                size: 18,
                color: '#7f7f7f'
            },
            showlegend: false,
            hovermode: this.orientation === "h" ? "y unified" : "x unified",
            yaxis: {automargin: true},
            xaxis: {automargin: true},
            margin:{
                t: 60
            }
        };

        this.config = { displayModeBar: false };
    }

    /**
     * 
     * Creates a plotCard as a child of an object with the given class name
     * 
     * @param {String} parentClassName 
     */
    createContainer(parentClassName) {
        var container = document.querySelector(parentClassName)
        container.insertAdjacentHTML("beforeend",`<div id="${this.plotName}" class="plot-card"></div>`);
    }

    /**
     * Renders the Plot Card to the container 
     */
    render() {
        if (typeof Plotly === 'undefined') {
            throw new Error('Plotly is not loaded');
        }
        Plotly.newPlot(this.plotName, this.formatData(), this.layout, this.config);
    }

    updateData(newData) {
        this.data = newData;
        return this;
    }

    updateLayout(newLayout) {
        this.layout = Object.assign({}, this.layout, newLayout);
        return this;
    }

    /**
     * Formats the PlotCards data to a format that is usable for plotly
     * @returns 
     */
    formatData(){
        var formattedData = [];
        console.log(this.data)
        for(var idx in this.data){
            var trace = this.data[idx]
            var formattedTrace = {x: [], y: [], name: trace.name, orientation:this.orientation, type: "bar", hovertemplate: null, marker: {color: '#ee2e32'}}
            if(this.orientation === "h"){
                formattedTrace.x = trace.values;
                formattedTrace.y = trace.labels;
            } else {
                formattedTrace.x = trace.labels;
                formattedTrace.y = trace.values;
            }
            if(trace.color) formattedTrace.marker.color = trace.color;

            formattedData.push(formattedTrace);
        }
        console.log(formattedData)
        return formattedData;
    }
}