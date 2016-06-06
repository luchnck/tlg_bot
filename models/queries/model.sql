{% sql 'select_from_where', note="template for standart sql query SELECT. variables are table, [fields], [conds], [limit]" %}
	SELECT {% if fields %} `{{fields|join('`,`')}}` {% else %} * {% endif %}
	FROM {{ table }}
	{% if conds %}
	WHERE 	{% for cond,value in conds.items() %}
			{% if loop.index0 > 0 %} AND {% endif %}
			{{cond}} = {{value}} 
		{% endfor %}
	{% endif %}
	{% if limit %}
	LIMIT {{limit}}
	{% endif %};
{% endsql %}

{% sql 'conditions', note = "rendering conditions WHERE" %}
        
{% endsql %}
