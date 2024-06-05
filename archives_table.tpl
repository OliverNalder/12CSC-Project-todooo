%#template to generate a HTML table from tuples (or list of lists, or tuple or tuples or ...)
<link href='/static/style.css' rel='stylesheet'>
<div class="help"><a href='/help'>?</a></div>
<h1>ToDo List</h1>
<p>The open items are as follows:</p>
<table border="1">
%num = 0
%for row in rows:
    %num += 1
    
    <tr>
    %for col in row:
        <td>{{col}}</td>
    %end
    
    <td><a href='/edit/{{row[0]}}'>edit</a></td>
    </tr>
%end
</table>

<table>

    <td>
    <a href='/todo'>Back</a>
    </td>

</table>
