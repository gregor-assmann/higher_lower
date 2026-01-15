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
            plot_bgcolor: options.color ?? "rgba(38, 39, 43, 0)",
            paper_bgcolor: options.color ?? "rgba(38, 39, 43, 0)",
            hoverlabel:{ 
                bgcolor: "rgba(149, 153, 165, 1)", 
                font: {            
                    color: 'rgba(46, 48, 55, 1)'
                },
                bordercolor: "rgba(149, 153, 165, 1)",      // set your desired border color here
                borderradius: "5"},
            font: {
                family: 'Arial',
                color: '#7f7f7f'
            },
            showlegend: false,
            hovermode: this.orientation === "h" ? "y unified" : "x unified",
            yaxis: {automargin: true, showgrid: false,},
            xaxis: {automargin: true, showgrid: false,},
            margin:{
                t: 40,
                l: 0,
                r: 0,
                b: 0
            },
        };

        this.config = { displayModeBar: false };
    }

    /**
     * 
     * Creates a plotCard as a child of an object with the given class name
     * 
     * @param {String} parentClassName 
     */
    createInContainer(parentClassName) {
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
        this.setFontSize()
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

    setFontSize(){
        let currentLayout = this.layout
        currentLayout.font.size = Math.ceil(window.innerHeight/100)
        console.log(Math.floor(window.innerHeight/100))
        this.updateLayout(currentLayout)
    }

    /**
     * Formats the PlotCards data to a format that is usable for plotly
     * @returns 
     */
    formatData(){
        var formattedData = [];
        for(var idx in this.data){
            var trace = this.data[idx]
            var formattedTrace = {x: [], y: [], name: trace.name, orientation:this.orientation, type: "bar", hovertemplate: null, marker: {color: trace.color??'#ee2e32'}}
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
        return formattedData;
    }
}

const cards=[]


document.addEventListener("DOMContentLoaded", async () => {
    createCard("/getstats?data=games-by-name", "h", "Games by Name");
    createCard("/getstats?data=games-by-date", "v", "Games by Date");
    createCard("/getstats?data=score-by-date", "v", "Total Score by Date");
    createCard("/getstats?data=topscore-by-name", "h", "Highscore by Name");
});

window.addEventListener("resize", () => {
    cards.forEach(card => card.render())
})

async function getData(link){
   try {
    const response = await fetch(link);

    if(!response.ok) throw new Error("Error fetching Data")
    
    const data = await response.json()
    return data;
   } catch(error) {
    console.error("Error parsing Data: ", error)
    return null;
   }
}
async function createCard(link, orientation, title){
    try {
        const data = await getData(link);
        if (!data) { console.error("No data received for score-by-date"); return;}
        var traces = []
        
        const labels = data[0].labels;
        const valueIds = data[0]['value-ids'];
        const values = data[0].values;
        const colorMap = {normal: 'rgb(236, 214, 100)', hard: 'rgb(236, 156, 100)', extreme: 'rgb(236, 110, 100)', value:"#ee2e32"}
        
        //pad labels with whitespaces to avoid same labels being merged
        const padLabel = (labels) => labels.map((label, idx) => {for(let i = 0; i < idx; i++) label = " " + label; return label})

        valueIds.forEach((id) => {
        const trace = {
            name: id,
            labels: padLabel(labels),
            values: values.map(item => item[id] || 0),
            color: colorMap[id]
            };
            traces.push(trace);
    });
        
        console.log(traces)

        const card = new PlotCardBar(title.toLowerCase().split(" ").join("-"), {title: title, orientation: orientation, data: traces});
        card.createInContainer(".stat-container")
        card.render()
        cards.push(card)
    } catch (err) {
        console.error(err);
        return null
    }
}
