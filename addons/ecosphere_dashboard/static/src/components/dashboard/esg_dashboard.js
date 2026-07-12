odoo.define('ecosphere_dashboard.esg_dashboard', function (require) {
    'use strict';

    var core = require('web.core');
    var Widget = require('web.Widget');
    var ajax = require('web.ajax');
    var QWeb = core.qweb;

    var ESGDashboard = Widget.extend({
        template: 'ecosphere_dashboard.esg_dashboard',
        init: function (parent, options) {
            this._super(parent, options);
            this.data = {
                company: '',
                environmental_score: 0,
                social_score: 0,
                governance_score: 0,
                department_ranking: [],
                leaderboard: [],
                carbon_trend: [],
            };
        },
        start: function () {
            var self = this;
            this._super();
            ajax.jsonRpc('/ecosphere/dashboard/data', 'call', {}).then(function (result) {
                self.data = result;
                self.renderCharts();
                self.$el.html(QWeb.render('ecosphere_dashboard.esg_dashboard', {widget: self, data: self.data}));
            });
            return this;
        },
        renderCharts: function () {
            this.renderScoreChart('environmental-score-chart', this.data.environmental_score, '#4CAF50');
            this.renderScoreChart('social-score-chart', this.data.social_score, '#2196F3');
            this.renderScoreChart('governance-score-chart', this.data.governance_score, '#FF9800');
            this.renderBarChart('department-ranking-chart', this.data.department_ranking);
            this.renderLeaderboardChart('leaderboard-chart', this.data.leaderboard);
            this.renderTrendChart('carbon-trend-chart', this.data.carbon_trend);
        },
        renderScoreChart: function (elementId, value, color) {
            var chart = document.getElementById(elementId);
            if (!chart) {
                return;
            }
            var myChart = echarts.init(chart);
            var option = {
                series: [{
                    type: 'gauge',
                    startAngle: 180,
                    endAngle: 0,
                    min: 0,
                    max: 100,
                    splitNumber: 10,
                    axisLine: { lineStyle: { width: 20, color: [[1, '#e8e8e8']] } },
                    pointer: { length: '70%', width: 6 },
                    axisTick: { distance: -20, length: 8, lineStyle: { color: '#999' } },
                    splitLine: { distance: -20, length: 20, lineStyle: { color: '#999' } },
                    anchor: { show: true, showAbove: true, size: 15, itemStyle: { color: color } },
                    title: { offsetCenter: ['0%', '-30%'] },
                    detail: { valueAnimation: true, fontSize: 24, offsetCenter: ['0%', '0%'], formatter: '{value}%' },
                    data: [{ value: value, name: 'Score' }],
                    itemStyle: { color: color },
                }]
            };
            myChart.setOption(option);
        },
        renderBarChart: function (elementId, data) {
            var chart = document.getElementById(elementId);
            if (!chart) {
                return;
            }
            var myChart = echarts.init(chart);
            var option = {
                tooltip: { trigger: 'axis' },
                xAxis: { type: 'category', data: data.map(function (item) { return item.name; }) },
                yAxis: { type: 'value' },
                series: [{ type: 'bar', data: data.map(function (item) { return item.score; }), color: '#4CAF50' }],
            };
            myChart.setOption(option);
        },
        renderLeaderboardChart: function (elementId, data) {
            var chart = document.getElementById(elementId);
            if (!chart) {
                return;
            }
            var myChart = echarts.init(chart);
            var option = {
                tooltip: { trigger: 'item' },
                xAxis: { type: 'value' },
                yAxis: { type: 'category', data: data.map(function (item) { return item.name; }) },
                series: [{ type: 'bar', data: data.map(function (item) { return item.score; }), color: '#2196F3' }],
            };
            myChart.setOption(option);
        },
        renderTrendChart: function (elementId, data) {
            var chart = document.getElementById(elementId);
            if (!chart) {
                return;
            }
            var myChart = echarts.init(chart);
            var option = {
                tooltip: { trigger: 'axis' },
                xAxis: { type: 'category', data: data.map(function (item) { return item.name; }) },
                yAxis: { type: 'value' },
                series: [{ type: 'line', data: data.map(function (item) { return item.value; }), smooth: true, color: '#FF5722' }],
            };
            myChart.setOption(option);
        },
    });

    core.define('ecosphere_dashboard.esg_dashboard', ESGDashboard);
    return ESGDashboard;
});
