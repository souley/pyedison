import Chart from 'chart.js'

export class MyBarchart {

    private myChart: Chart

    constructor(ctx: string, labels: Array<string>, values: Array<number>, title: string){
        this.myChart = this.getCharWithParams(ctx, labels, values, title)
    }

    public redrawGraph(ctx: string, labels: Array<string>, values: Array<number>, title: string){
        this.myChart.destroy()
        this.myChart = this.getCharWithParams(ctx, labels, values, title)
    }

    private getCharWithParams(ctx: string, labels: Array<string>, values: Array<number>, title: string){
        var backgroundColors =  ['rgba(255, 99, 132, 0.2)', 'rgba(54, 162, 235, 0.2)', 'rgba(255, 206, 86, 0.2)', 'rgba(75, 192, 192, 0.2)', 'rgba(153, 102, 255, 0.2)', 'rgba(255, 159, 64, 0.2)'];
        var borderColors = [ 'rgba(255,99,132,1)', 'rgba(54, 162, 235, 1)', 'rgba(255, 206, 86, 1)', 'rgba(75, 192, 192, 1)', 'rgba(153, 102, 255, 1)', 'rgba(255, 159, 64, 1)'];

        while(backgroundColors.length < labels.length){
            backgroundColors = backgroundColors.concat(backgroundColors);
            borderColors = borderColors.concat(borderColors);
        }

        backgroundColors = backgroundColors.slice(0, labels.length)
        borderColors = borderColors.slice(0, labels.length)

        return  new Chart(ctx, {
            type: 'bar',
            data: {labels: labels,
            datasets: [
                {
                    label: title,
                    backgroundColor: backgroundColors,
                    borderColor: borderColors,
                    borderWidth: 1,
                    data: values,
                }
            ]},
            options: {
                scales: {
                    xAxes: [{
                        stacked: true
                    }],
                    yAxes: [{
                        stacked: true
                    }]
                },
                responsive: false
                }
            });
        }

}