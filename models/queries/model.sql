{% sql 'select_from_where', note="template for standart sql query SELECT. variables are table, [fields], [conds], [limit]" %}
	SELECT {% if fields %} {{fields|join(',')}} {% else %} * {% endif %}
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

{% sql 'update_table_set', note = "rendering update query, variables are table, vals, where " %}
	UPDATE {{ table }}
        {% if vals %}
	SET {% for cond,value in vals.items() %}
	 		{% if loop.index0 > 0 %},{% endif %}
                        	{{cond}} = {{value}}
	    {% endfor %}
        {% endif %}
        {% if where %}
	WHERE  {% for cond,value in where.items() %}
                        {% if loop.index0 > 0 %} AND {% endif %}
                                {{cond}} = {{value}}
                {% endfor %};
        {% endif %}
        
{% endsql %}
