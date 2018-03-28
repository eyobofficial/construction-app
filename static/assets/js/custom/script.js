$(document).ready(function(){

    // Project list datatables
    $('#projectDatatables').DataTable({
        "pagingType": "full_numbers",
        "lengthMenu": [
            [10, 25, 50, -1],
            [10, 25, 50, "All"]
        ],
        "order": [],
        responsive: true,
        language: {
            search: "_INPUT_",
            searchPlaceholder: "Search projects",
        }
    });

    // Generic datatables
    $('#datatables').DataTable({
        "pagingType": "full_numbers",
        "lengthMenu": [
            [10, 25, 50, -1],
            [10, 25, 50, "All"]
        ],
        responsive: true,
        language: {
            search: "_INPUT_",
            searchPlaceholder: "Search records",
        }

    });
});