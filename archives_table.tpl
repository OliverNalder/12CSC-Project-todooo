%#template to generate a HTML table from tuples (or list of lists, or tuple or tuples or ...)
<link href='/static/style.css' rel='stylesheet'>
<div class="help"><a href='/help'>?</a></div>
<h1>The Archive</h1>
%if rows != []:
    <p>The open items are as follows:</p>
    <table border="1">
    %num = 0
    %for row in rows:
        %num += 1
        
        <tr>
        <td class='arch_td'>ID: {{row[0]}}</td>
        <td>{{row[1]}}</td>

        <td class="alt_td"><a href='/edit/{{row[0]}}'>edit</a></td>
        </tr>
    %end
    </table>

    <table>

        <td class="alt_td">
        <a href='/todo' class="alt_td"><button>Back</button></a>
        </td>
        <td class="alt_td">
        <a href='/archive_all/1' class="alt_td"><button>Unarchive all</button></a>
        </td>

    </table>

%else:
    <table>
        <td class="alt_td">
        <a href='/todo' class="alt_td"><button>Back</button></a>
        </td>
    </table>