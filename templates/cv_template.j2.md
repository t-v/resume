# {{ info.firstname }} {{ info.surname }}

{% if 'quote' in info.keys() %}
{{ info.quote }}
{% endif %}
## Personal data

Name: {{ info.firstname }} {{ info.surname }}  
Date of birth: {{ info.birth }}  
Citizenship: {{ info.nationality }}  
Gender: {{ info.gender }}  
Function: {{ info.label }}  
City: {{ info.city }}

## Contact information

Address: {{ location.address }}  
City: {{ location.code }} {{ location.city }}  
Country: {{ location.country }}

{% if contact.website is defined %}
Website: <{{ contact.website }}>  
{% endif %}
Phone: {{ contact.phone }}  
{% if contact.fax is defined %}
Fax: {{ contact.fax }}  
{% endif %}
Mail: {{ contact.email }}  

{% if references is defined %}
## References

{% for reference in references %}
**{{ reference.name }}**  
_{{ reference.function }}_  
{{ reference.company }}

{% endfor %}
{% endif %}
{% if social is defined %}
## Social

{% for social_project in social %}
{{ social_project.label }}  
URL: <{{ social_project.url }}>

{% endfor %}
{% endif %}
{% if projects is defined %}
## Personal Projects
{% for project in projects %}

### {{ project.title }}

URL: <{{ project.url }}>  
{% if project. description is defined %}Description: {{ project.description }}{% endif %}  
{% if project.role is defined %}Role: {{ project.role }}{% endif %}  
{% if project.summary is defined %}Input: {{ project.summary }}{% endif %}

{% endfor %}
{% endif %}

## Employment

{% if employment.summary is defined %}
{{ employment.summary }}
{% endif %}
{% for job in employment.history %}

### {{ job.employer }}

{% if job.url is defined %}
URL: <{{ job.url }}>  
{% endif %}
Position: {{ job.position }}  
Term: {{ job.start }} > {% if job.current %}now{% else %}{{ job.end }}{{ end }}{% endif %}  
{% if job.summary is defined and job.summary != '' %}
Summary: {{ job.summary }}
{% endif %}
{% if job.highlights is defined %}
Highlights:

{% for jobhighlight in job.highlights %}
- {{ jobhighlight }}
{% endfor %}

{% endif %}
{% if job.keywords is defined %}
Keywords:

{% for jobkey in job.keywords %}
- {{ jobkey }}
{% endfor %}
{% endif %}
{% endfor %}

## Languages

{% for language in languages %}
{{ language.language }}: {{ language.level }}  
{% endfor %}

## Skills

{% for skillset in skills.sets %}
### {{ skillset.name }}

_{{ skillset.level }}_

{% for skill in skillset.skills %}
{{ skill.name }}: {{ skill.level }}  
{% endfor %}

{% endfor %}
