const input = [{}];
var result = [];

function toCSV(items) {
if (items) {
    items.forEach(function(a) {
        result.push({
          0: a.holder,
          1: a.Position + '/' + a.pct.shares_out
        });
        toCSV(a.Node);
    });
  }
}
  toCSV(input);
console.log(result);

