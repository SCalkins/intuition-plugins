{% extends "panel.tpl" %}

{% block build %}
    {% for dashboard in panel %}
        d{{ dashboard.i }} = Dashboard.create!(:name => "{{ dashboard['title'] }}")

        # Create graph widgets
        d{{ dashboard.i }}.widgets.create!(
            :name => "Portfolio Value", :kind => "graph",
            :size_x => 2, :size_y => 2,
            :source => 'http_proxy',
            :settings => {
                :graph_type => 'area',
                :range => "24-hours",
                :proxy_url => "http://127.0.0.1:5000/api/v1/portfolios?id={{ dashboard.portfolio }}&key=portfolio.portfolio_value",
                :targets => "{{ dashboard.portfolio }}.portfolio_value"})
        d{{ dashboard.i }}.widgets.create!(
            :name => "Max Drawdown", :kind => "graph",
            :size_x => 1, :size_y => 2,
            :source => 'http_proxy',
            :settings => {
                :graph_type => 'line',
                :range => "24-hours",
                :proxy_url => "http://{{ dashboard.proxy_ip }}:{{ dashboard.proxy_port }}/api/v1/portfolios?id={{ dashboard.portfolio }}&key=cmr.max_drawdown",
                :targets => "{{ dashboard.portfolio }}.max_drawdown"})

        # Create Number widgets
        d{{ dashboard.i }}.widgets.create!(
            :name => "Portfolio return", :kind => 'number', :size_x => 2, :source => 'http_proxy',
            :settings => {
                :label => "%",
                :proxy_url => "http://{{ dashboard.proxy_ip }}:{{ dashboard.proxy_port }}/api/v1/portfolios?id={{ dashboard.portfolio }}&key=portfolio.returns",
                :proxy_value_path => "{{ dashboard.portfolio }}.returns" })
        d{{ dashboard.i }}.widgets.create!(
            :name => "PNL", :kind => 'number', :source => 'http_proxy',
            :settings => {
                :label => " ",
                :proxy_url => "http://{{ dashboard.proxy_ip }}:{{ dashboard.proxy_port }}/api/v1/portfolios?id={{ dashboard.portfolio }}&key=portfolio.pnl",
                :proxy_value_path => "{{ dashboard.portfolio }}.pnl"})
        d{{ dashboard.i }}.widgets.create!(
            :name => "Sortino Ratio", :kind => 'number', :source => 'http_proxy',
            :settings => {
                :label => " ",
                :proxy_url => "http://{{ dashboard.proxy_ip }}:{{ dashboard.proxy_port }}/api/v1/portfolios?id={{ dashboard.portfolio }}&key=cmr.sortino",
                :proxy_value_path => "{{ dashboard.portfolio }}.sortino"})
        d{{ dashboard.i }}.widgets.create!(
            :name => "Volatility", :kind => 'number', :size_x => 1, :source => 'http_proxy',
            :settings => {
                :label => " ",
                :proxy_url => "http://{{ dashboard.proxy_ip }}:{{ dashboard.proxy_port }}/api/v1/portfolios?id={{ dashboard.portfolio }}&key=cmr.algo_volatility",
                :proxy_value_path => "{{ dashboard.portfolio }}.algo_volatility" })
        d{{ dashboard.i }}.widgets.create!(
            :name => "Value", :kind => 'number', :size_x => 2, :source => 'http_proxy',
            :settings => {
                :label => "$", :proxy_url => "http://{{ dashboard.proxy_ip }}:{{ dashboard.proxy_port }}/api/v1/portfolios?id={{ dashboard.portfolio }}&key=portfolio.portfolio_value",
                :proxy_value_path => "{{ dashboard.portfolio }}.portfolio_value" })
        d{{ dashboard.i }}.widgets.create!(
            :name => "Benchmark return", :kind => 'number', :source => 'http_proxy',
            :settings => {
                :label => "%",
                :proxy_url => "http://{{ dashboard.proxy_ip }}:{{ dashboard.proxy_port }}/api/v1/portfolios?id={{ dashboard.portfolio }}&key=cmr.benchmark_period_return",
                :proxy_value_path => "{{ dashboard.portfolio }}.benchmark_period_return" })

        # Create Boolean widgets
        d{{ dashboard.i }}.widgets.create!(
            :name => "App Health", :kind => 'boolean', :source => 'shell',
            :settings => {
                :label => "Runtime",
                :command => "ps -a | grep deploy" })
        d{{ dashboard.i }}.widgets.create!(
            :name => "Portfolio Health", :kind => 'boolean', :source => 'http_proxy',
            :settings => {
                :label => "trend",
                :proxy_url => "http://{{ dashboard.proxy_ip }}:{{ dashboard.proxy_port }}/api/v1/portfolios?id={{ dashboard.portfolio }}&key=portfolio.returns",
                :proxy_value_path => "{{ dashboard.portfolio }}.returns" })
    {% endfor %}
{% endblock %}
