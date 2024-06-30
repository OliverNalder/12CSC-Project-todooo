%#template to generate a HTML table from tuples (or list of lists, or tuple or tuples or ...)
<link href='/static/style.css' rel='stylesheet'>
<div class="help"><a href='/help'>?</a></div>
<h1>To Do List</h1>
<div class="sorting">
    <form method="GET">
        <select name="Sort_By">
            <option selected disabled hidden>Sort By:</option>
            <option>name</option>
            <option>priority</option>
            <option>progress</option>
        </select>
        <select name="Order" placeholder="Order">
            <option selected disabled hidden>Order:</option>
            <option>descending</option>
            <option>ascending</option>
        </select>
        <input type="submit" name="save" value="save">
    </form>
</div>

%if rows != []:
    <p>The open items are as follows:</p>
    <table border="1">
    %num = 0

    %for row in rows:
        %num += 1
        %count = 0
        <tr>
        <td>{{num}}</td>
            <td>
                <div class="task_name">
                    {{row[1]}}
                </div>
                <form method="GET">
                    <div class="progress_container">
                        
                        <div class="slidecontainer">
                            <div class="progress_value">
                                <p>Progress: {{(12.5*row[2])}}%</p>
                            </div>
                            <input type="range" min="0" max="8" value="{{row[2]}}" name="slider" class="slider" id="{{row[2]}}">
                        </div>
                        <div class="slider_save">
                            <input type="submit" value="save" name="progress_save">
                        </div>
                    </div>
                    <input type="hidden" value="{{row[0]}}" name="value_id">
                </form>
            </td>
        
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
    <td>
    <a href='/archive_all/0'>Archive all</a>
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


