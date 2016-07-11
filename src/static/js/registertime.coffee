$timeField = $("#time")

currentTime = ->
    currentValue = parseInt $timeField.val()
    if currentValue
        currentValue
    else
        0

$addButton = $("#addition")
$addButton.click ->
    $timeField.val(currentTime()+1)
$subtractButton = $("#subtract")
$subtractButton.click ->
    $timeField.val(currentTime()-1)
