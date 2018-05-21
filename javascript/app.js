// create some array
const numbers = [43,32,77,1,2,3];
const numbers2 = new Array(22,45,33,76,54);
const fruit = ['Apple','Banana','Orange','Pear'];
const mixed = [22, 'hello', true, undefined, null, {a:1,b:1}, new Date()];

let val;

// get array length
val = numbers.length;
val = Array.isArray(numbers);

val = numbers[3];
val = numbers[0];

// insert in to array
numbers[2] = 100;
val = numbers.indexOf(3);

numbers.push(250)




console.log(numbers);
console.log(val);