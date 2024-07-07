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
            <option value="due">Due Date</option>
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
            <td class="table_height">{{num}}</td>
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
        <td>
            <div class="due_date">
                Due:<br>{{row[3][-2]}}{{row[3][-1]}}/{{row[3][-5]}}{{row[3][-4]}}/{{row[3][0]}}{{row[3][1]}}{{row[3][2]}}{{row[3][3]}}
            </div>
        </td>
        <td class="alt_td"><a href='/view/{{row[0]}}'>View</a></td>
        <td class="alt_td"><a href='/edit/{{row[0]}}'>edit</a></td>

        </tr>

    %end
    </table>

    <table>
        <td class="alt_td">
        <a href='/' class="alt_td"><button>Main Page</button></a>
        </td>
        <td class="alt_td">
        <a href='/new' border='1' class="alt_td"><button>New Task</button></a>
        </td>
        <td class="alt_td">
        <a href='/closed' border='1' class="alt_td"><button>Archived</button></a>
        </td>
        <td class="alt_td">
        <a href='/archive_all/0' class="alt_td"><button>Archive all</button></a>
        </td>
    </div>
    </table>
%else:
    <p>There are no items in your To Do list</p>
    <table>

    <td class="alt_td">
    <a href='/' class="alt_td"><button>Main Page</button></a>
    </td>
    <td class="alt_td">
    <a href='/new' border='1' class="alt_td"><button>New Task</button></a>
    </td>
    <td class="alt_td">
    <a href='/closed' border='1' class="alt_td"><button>Archived</button></a>
    </td>

    </table>


