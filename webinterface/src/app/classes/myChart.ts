import Chart from 'chart.js'

export class MyChart {
    myChart: Chart;

  constructor(selector: string, labels: Array<string>, label1: string, data1: Array<number>,
    label2: string, data2: Array<number>) {
      this.myChart = this.getChartWithParams(selector, labels, label1, data1,
        label2, data2);
  }

  redrawGraph(selector: string, labels: Array<string>, label1: string, data1: Array<number>,
    label2: string, data2: Array<number>) : void {
        this.myChart.destroy();
        this.myChart = this.getChartWithParams(selector, labels, label1, data1,
          label2, data2);
    }

    private getChartWithParams(selector: string, labels: Array<string>, label1: string, data1: Array<number>,
      label2: string, data2: Array<number>): Chart {
          return new Chart(selector, {
            type: 'radar',
            data: {
              labels: labels,
              datasets: [
                {
                  label: label1,
                  backgroundColor: "rgba(132,99,255,0.2)",
                  borderColor: "rgba(132,99,255,1)",
                  pointBackgroundColor: "rgba(179,181,198,1)",
                  pointBorderColor: "#fff",
                  pointHoverBackgroundColor: "#fff",
                  pointHoverBorderColor: "rgba(179,181,198,1)",
                  data: data1
                },
                {
                  label: label2,
                  backgroundColor: "rgba(255,99,132,0.2)",
                  borderColor: "rgba(255,99,132,1)",
                  pointBackgroundColor: "rgba(255,99,132,1)",
                  pointBorderColor: "#fff",
                  pointHoverBackgroundColor: "#fff",
                  pointHoverBorderColor: "rgba(255,99,132,1)",
                  data: data2
                }
              ]
            },
            options: {
              scale: {
                reverse: false,
                ticks: {
                  beginAtZero: true
                }
              }
            }
          });
      }
}
