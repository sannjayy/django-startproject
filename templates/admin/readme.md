- Added Favicon Image from > base.html

```html
<link rel="shortcut icon" href="{% static 'favicon.ico' %}" type="image/x-icon" />
```

- Added logo option in > base_site.html

```html
<div id="site-name">
    {% if env.USE_ADMIN_LOGO == 'True' %}
        <a href="{% url 'admin:index' %}"> <img src="{% static 'logo.png' %}" alt="{{site_header}}" title='{{site_header}}' style="height:40px"></a>
    {% else %}
        <a href="{% url 'admin:index' %}">{{ site_header|default:_('Znas administration') }}</a>
    {% endif %}
</div>
```