let arr= [1, 2, 3, 4, 5];
console.log(arr.length);

//add element at end
arr.push(6);
console.log(arr);

//remove element from end
arr.pop(6);
console.log(arr);

//push multiple elements
arr.push(6, 7, 8);
console.log(arr);

//add at begining
arr.unshift(0);
console.log(arr);

//remove from begining
arr.shift();
console.log(arr);

//add & remove the element from start, middle & end
arr.splice(2, 1, 10);
console.log(arr);

arr.splice(3, 2);
console.log(arr);

arr.splice(3, 2, 22, 12);
console.log(arr);




