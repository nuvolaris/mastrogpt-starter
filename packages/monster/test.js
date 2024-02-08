//--web true
//--kind nodejs:default
//--param MONGODB_URL $MONGODB_URL

const { MongoClient } = require("mongodb")

let db = null

function connectDB(uri) {
    const client = new MongoClient(uri)
    db = client.db('study_monster')    
}

async function main(args) {
    connectDB(args.MONGODB_URL)

    const _users = db.collection('users')
    const users = await _users.find().toArray()
    
    const response = {
        success: true,
        message: "OK",
        data: users
    }
    return { body: response }
}
