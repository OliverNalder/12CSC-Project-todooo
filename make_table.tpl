%#template to generate a HTML table from tuples (or list of lists, or tuple or tuples or ...)
<link href='/static/style.css' rel='stylesheet'>
<div class="help"><a href='/help'>?</a></div>
<h1>ToDo List</h1>
<p>The open items are as follows:</p>
%if rows != []:
    <table border="1">
    %num = 0

    %for row in rows:
        %num += 1
        %count = 0
        <tr>
        <td>{{num}}</td>

        
            <td>{{row[1]}}
            <form method="GET">
            <div class="slidecontainer">
                <input type="range" min="0" max="4" value="{{row[2]}}" name="slider" class="slider" id="{{row[0]}}">
            </div></td>
        </form>
        <td><a href='/view/{{row[0]}}'>View</a></td>
        <td><a href='/edit/{{row[0]}}'>edit</a></td>
        </tr>
    %end
    </table>

    <table>

    <td>
    <a href='/'>Main Page</a>
    </td>
    <td>
    <a href='/new' border='1'>New Task</a>
    </td>
    <td>
    <a href='/closed' border='1'>Archived</a>
    </td>

    </table>
%else:
    <table>

    <td>
    <a href='/'>Main Page</a>
    </td>
    <td>
    <a href='/new' border='1'>New Task</a>
    </td>
    

    </table>


