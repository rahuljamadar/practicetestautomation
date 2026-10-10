let arr= ["pass", "fail", "skip"];
console.log(arr.length);

arr.push("blocked");
console.log(arr);

arr.pop("blocked");
console.log(arr);

arr.unshift("picked");
console.log(arr);

arr.shift("picked");
console.log(arr);

arr.splice(2, 1, "picked");
console.log(arr);
