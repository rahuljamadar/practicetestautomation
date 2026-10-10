let status= ["pass", "fail", "skip"];
console.log(status.length);

console.log(status.at(-2));
console.log(status.at(-1));

//modify
status[2]= "Blocked";
console.log(status);
console.log("=======");
status[0]= "Picked";
console.log(status);