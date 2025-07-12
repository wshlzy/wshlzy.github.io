function send_ajax(databaseName) {
    $.ajax({
        //发送请求的url地址
        url:'/send_ajax',
        //发送请求的方式
        type:'post',
        //请求端携带的数据
        data: { database: databaseName },
        success:function () {
            //成功之后要执行的业务逻辑
            console.log("success")
        },
        error:function () {
            //失败后的业务逻辑
            console.log("发送ajax请求失败")
        }
    })
}

//饼图
document.addEventListener('DOMContentLoaded', function() {
    var databaseName = document.getElementById("databaseName").value.trim();
    var chartDom = document.getElementById('main');
    var myChart = echarts.init(chartDom);
    var option;

    // setInterval(send_ajax(databaseName), 1000);
    setInterval(function() {
        send_ajax(databaseName);
    }, 1000);

    // 获取数据
    function fetchData() {
        return fetch('../static/js/data.json')
            .then(response => response.json());
    }

    // 更新图表
    function updateChart(type) {
        fetchData()
            .then(data => {
                console.log('Fetched Data:', data);  // 调试信息

                // 获取所选类型的数据
                var typeData = data.find(item => item["graph_Name"] === type);

                // 准备饼图数据
                var pieData = [
                    { name: 'A', value: typeData["A"] },
                    { name: 'B', value: typeData["B"] },
                    { name: 'C', value: typeData["C"] },
                    { name: 'D', value: typeData["D"] },
                ];

                option = {
                    title: {
                        text: type + '题目选择情况',
                        left: 'center'
                    },
                    tooltip: {
                        trigger: 'item'
                    },
                    legend: {
                        orient: 'vertical',
                        left: 'left'
                    },
                    series: [
                        {
                            name: '选择情况',
                            type: 'pie',
                            radius: '50%',
                            data: pieData,
                            emphasis: {
                                itemStyle: {
                                    shadowBlur: 10,
                                    shadowOffsetX: 0,
                                    shadowColor: 'rgba(0, 0, 0, 0.5)'
                                }
                            }
                        }
                    ]
                };

                option && myChart.setOption(option);
            })
            .catch(error => console.error('Error fetching the data:', error));
    }

    // 初始化图表
    updateChart('第一类');

    // document.querySelectorAll('.type-button').forEach(button => {
    //     button.addEventListener('click', function() {
    //         var type = this.dataset.type;
    //         updateChart(type);
    //     });
    // });

    // // 添加搜索按钮点击事件
    // document.getElementById('type').addEventListener('click', function() {
    //     var typeButton = document.getElementById('type').value.trim();
    //     if (typeButton) {
    //         updateChart(typeButton);
    //     }
    // });

    document.querySelectorAll('#type').forEach(function(button) {
        button.addEventListener('click', function(event) {
            var typeButton = event.target.value.trim(); // 获取点击按钮的 value 值
            if (typeButton) {
                updateChart(typeButton); // 调用 updateChart 函数并传递按钮的 value 值
            }
        });
    });

    setInterval(fetchData,1000);
    setInterval(updateChart(type),1000);
});

//柱状图
function barchart() {
    var chartDom = document.getElementById('mainB');
    var myChart = echarts.init(chartDom);
    var option;

    // 获取数据
    function fetchData() {
        return fetch('../static/js/data2.json')
            .then(response => response.json());
    }

    function updateBarChart() {
        fetchData()
            .then(data => {
                console.log('Fetched Data:', data);  // 调试信息

                // 获取所选类型的数据
                var typeData = data.find(item => item["graph_Name"] === "histogram");

                var categories = ['第一类','第二类','第三类','第四类','第五类']
                //准备饼图数据
                var barData = [
                    {name: "第一类正确数量", value: typeData["第一类正确数量"]},
                    {name: "第二类正确数量", value: typeData["第二类正确数量"]},
                    {name: "第三类正确数量", value: typeData["第三类正确数量"]},
                    {name: "第四类正确数量", value: typeData["第四类正确数量"]},
                    {name: "第五类正确数量", value: typeData["第五类正确数量"]},
                ];

                option = {
                    title: {
                        text: '各类正确数量',
                        left: 'center'
                    },
                    xAxis: {
                        type: 'category',
                        data:  categories
                    },
                    yAxis: {
                        type: 'value',
                        interval: 1, // 设置 Y 轴刻度间隔为 1
                        minInterval: 1, // 最小刻度间隔为 1
                        axisLabel: {
                            formatter: function(value) {
                                return value.toFixed(0); // 保证标签为整数
                            }
                        }
                    },
                    series: [
                        {
                            data: barData,
                            type: 'bar'
                        }
                    ]
                };
                option && myChart.setOption(option);
            })
            .catch(error => console.error('Error fetching the data:', error));
    }
    // 初始化图表
    updateBarChart();

    setInterval(fetchData,1000);
    setInterval(updateBarChart,1000);
}
